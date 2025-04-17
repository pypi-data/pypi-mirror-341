import asyncio
import importlib.resources
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Optional, Text

import structlog
from jinja2 import Template

import rasa.shared.utils.io
from rasa.core.information_retrieval import SearchResult, SearchResultList
from rasa.dialogue_understanding.utils import add_prompt_to_message_parse_data
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.constants import (
    LLM_CONFIG_KEY,
    MODEL_CONFIG_KEY,
    OPENAI_PROVIDER,
    PROMPT_TEMPLATE_CONFIG_KEY,
    PROVIDER_CONFIG_KEY,
    TEXT,
    TIMEOUT_CONFIG_KEY,
)
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.exceptions import FileIOException, ProviderClientAPIException
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.providers.llm.llm_client import LLMClient
from rasa.shared.providers.llm.llm_response import LLMResponse
from rasa.shared.utils.health_check.health_check import perform_llm_health_check
from rasa.shared.utils.health_check.llm_health_check_mixin import LLMHealthCheckMixin
from rasa.shared.utils.llm import (
    DEFAULT_OPENAI_GENERATE_MODEL_NAME,
    DEFAULT_OPENAI_MAX_GENERATED_TOKENS,
    get_prompt_template,
    llm_factory,
    resolve_model_client_config,
    tracker_as_readable_transcript,
)

TYPE_CONFIG_KEY = "type"
EMBEDDING_MODEL_KEY = "embedding_model_name"

DEFAULT_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DOCUMENT_POST_PROCESSOR_PROMPT_FILE_NAME = (
    "document_post_processor_prompt_template.jina2"
)
DEFAULT_LLM_CONFIG = {
    PROVIDER_CONFIG_KEY: OPENAI_PROVIDER,
    MODEL_CONFIG_KEY: DEFAULT_OPENAI_GENERATE_MODEL_NAME,
    "temperature": 0.3,
    "max_tokens": DEFAULT_OPENAI_MAX_GENERATED_TOKENS,
    TIMEOUT_CONFIG_KEY: 5,
}
DEFAULT_DOCUMENT_POST_PROCESSOR_PROMPT_TEMPLATE = importlib.resources.read_text(
    "rasa.document_retrieval",
    "document_post_processor_prompt_template.jinja2",
)

structlogger = structlog.get_logger()


class PostProcessingType(Enum):
    PLAIN = "PLAIN"
    AGGREGATED_SUMMARY = "AGGREGATED_SUMMARY"
    INDIVIDUAL_SUMMARIES = "INDIVIDUAL_SUMMARIES"
    BINARY_LLM = "BINARY_LLM"
    BINARY_EMBEDDING_MODEL = "BINARY_EMBEDDING_MODEL"
    FINAL_ANSWER = "FINAL_ANSWER"

    def __str__(self) -> str:
        return self.value


class DocumentPostProcessor(LLMHealthCheckMixin):
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """The default config for the document post processor."""
        return {
            TYPE_CONFIG_KEY: PostProcessingType.PLAIN,
            LLM_CONFIG_KEY: DEFAULT_LLM_CONFIG,
            PROMPT_TEMPLATE_CONFIG_KEY: DEFAULT_DOCUMENT_POST_PROCESSOR_PROMPT_TEMPLATE,
        }

    def __init__(
        self,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        prompt_template: Optional[str] = None,
    ):
        self.config = {**self.get_default_config(), **config}
        self.config[LLM_CONFIG_KEY] = resolve_model_client_config(
            self.config.get(LLM_CONFIG_KEY), DocumentPostProcessor.__name__
        )
        self.prompt_template = prompt_template or get_prompt_template(
            config.get(PROMPT_TEMPLATE_CONFIG_KEY),
            DEFAULT_DOCUMENT_POST_PROCESSOR_PROMPT_TEMPLATE,
        )

        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> "DocumentPostProcessor":
        """Load document post processor."""
        llm_config = resolve_model_client_config(config.get(LLM_CONFIG_KEY, {}))
        perform_llm_health_check(
            llm_config,
            DEFAULT_LLM_CONFIG,
            "document_post_processor.load",
            DocumentPostProcessor.__name__,
        )

        # load prompt template
        prompt_template = None
        try:
            with model_storage.read_from(resource) as path:
                prompt_template = rasa.shared.utils.io.read_file(
                    path / DOCUMENT_POST_PROCESSOR_PROMPT_FILE_NAME
                )
        except (FileNotFoundError, FileIOException) as e:
            structlogger.warning(
                "document_post_processor.load_prompt_template.failed",
                error=e,
                resource=resource.name,
            )

        return DocumentPostProcessor(config, model_storage, resource, prompt_template)

    def persist(self) -> None:
        with self._model_storage.write_to(self._resource) as path:
            rasa.shared.utils.io.write_text_file(
                self.prompt_template, path / DOCUMENT_POST_PROCESSOR_PROMPT_FILE_NAME
            )

    async def process_documents(
        self,
        message: Message,
        search_query: str,
        documents: SearchResultList,
        tracker: DialogueStateTracker,
    ) -> SearchResultList:
        processing_type = self.config.get(TYPE_CONFIG_KEY)

        llm = llm_factory(self.config.get(LLM_CONFIG_KEY), DEFAULT_LLM_CONFIG)

        if processing_type == PostProcessingType.AGGREGATED_SUMMARY.value:
            return await self._create_aggregated_summary(documents, llm)

        elif processing_type == PostProcessingType.INDIVIDUAL_SUMMARIES.value:
            return await self._create_individual_summaries(documents, llm)

        elif processing_type == PostProcessingType.BINARY_LLM.value:
            return await self._check_documents_relevance_to_user_query(
                message, search_query, documents, llm, tracker
            )

        elif processing_type == PostProcessingType.BINARY_EMBEDDING_MODEL.value:
            return (
                await self._check_documents_relevance_to_user_query_using_modern_bert(
                    search_query,
                    documents,
                )
            )

        elif processing_type == PostProcessingType.PLAIN.value:
            return documents

        elif processing_type == PostProcessingType.FINAL_ANSWER.value:
            return await self._generate_final_answer(message, documents, llm, tracker)

        else:
            raise ValueError(f"Invalid postprocessing type: {processing_type}")

    @lru_cache
    def compile_template(self, template: str) -> Template:
        """Compile the prompt template.

        Compiling the template is an expensive operation,
        so we cache the result.
        """
        return Template(template)

    def render_prompt(self, data: Dict) -> str:
        # TODO: This should probably be fixed, as the default prompt template is empty
        #       If there are default templates for summarization they should be created,
        #       and ideally be initialized based on the processing type.
        prompt_template = get_prompt_template(
            self.config.get(PROMPT_TEMPLATE_CONFIG_KEY),
            DEFAULT_DOCUMENT_POST_PROCESSOR_PROMPT_TEMPLATE,
        )
        return self.compile_template(prompt_template).render(**data)

    async def _invoke_llm(self, prompt: str, llm: LLMClient) -> Optional[LLMResponse]:
        try:
            return await llm.acompletion(prompt)
        except Exception as e:
            # unfortunately, langchain does not wrap LLM exceptions which means
            # we have to catch all exceptions here
            structlogger.error("document_post_processor.llm.error", error=e)
            raise ProviderClientAPIException(
                message="LLM call exception", original_exception=e
            )

    async def _create_aggregated_summary(
        self, documents: SearchResultList, llm: LLMClient
    ) -> SearchResultList:
        prompt = self.render_prompt(
            {"retrieval_results": [doc.text for doc in documents.results]}
        )

        llm_response = await self._invoke_llm(prompt, llm)
        aggregated_summary = LLMResponse.ensure_llm_response(llm_response)

        aggregated_result = SearchResult(
            text=aggregated_summary.choices[0], metadata={}
        )

        return SearchResultList(results=[aggregated_result], metadata={})

    async def _create_individual_summaries(
        self, documents: SearchResultList, llm: LLMClient
    ) -> SearchResultList:
        tasks = []

        for doc in documents.results:
            prompt_template = self.render_prompt({"retrieval_results": doc.text})
            prompt = prompt_template.format(doc.text, llm)
            tasks.append(asyncio.create_task(self._invoke_llm(prompt, llm)))

        llm_responses = await asyncio.gather(*tasks)
        summarized_contents = [
            LLMResponse.ensure_llm_response(summary) for summary in llm_responses
        ]

        results = [
            SearchResult(text=summary.choices[0], metadata={})
            for summary in summarized_contents
        ]
        return SearchResultList(results=results, metadata={})

    async def _check_documents_relevance_to_user_query(
        self,
        message: Message,
        search_query: str,
        documents: SearchResultList,
        llm: LLMClient,
        tracker: DialogueStateTracker,
    ) -> SearchResultList:
        # If no documents were retrieved from the vector store, the
        # documents seem to be irrelevant. Respond with "NO".
        if not documents.results:
            return SearchResultList(
                results=[
                    SearchResult(
                        text="NO",
                        metadata={},
                    )
                ],
                metadata={},
            )

        prompt_data = {
            "search_query": search_query,
            "relevant_documents": documents,
            "conversation": tracker_as_readable_transcript(tracker, max_turns=10),
        }

        prompt = self.render_prompt(prompt_data)

        llm_response = await self._invoke_llm(prompt, llm)
        documents_relevance = LLMResponse.ensure_llm_response(llm_response)

        aggregated_result = SearchResult(
            text=documents_relevance.choices[0],
            metadata={},
        )

        add_prompt_to_message_parse_data(
            message=message,
            component_name=self.__class__.__name__,
            prompt_name="document_post_processor",
            user_prompt=prompt,
            llm_response=llm_response,
        )
        structlogger.debug(
            "document_post_processor._check_documents_relevance_to_user_query",
            prompt=prompt,
            documents=[d.text for d in documents.results],
            llm_response=llm_response,
        )

        return SearchResultList(results=[aggregated_result], metadata={})

    async def _check_documents_relevance_to_user_query_using_modern_bert(
        self,
        search_query: str,
        documents: SearchResultList,
        threshold: float = 0.5,
    ) -> SearchResultList:
        import torch
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            self.config.get(EMBEDDING_MODEL_KEY, DEFAULT_EMBEDDING_MODEL_NAME),
            trust_remote_code=True,
        )

        query_embeddings = self.model.encode(["search_query: " + search_query])
        doc_embeddings = self.model.encode(
            ["search_document: " + doc.text for doc in documents.results]
        )

        similarities = self.model.similarity(query_embeddings, doc_embeddings)

        is_any_doc_relevant = torch.any(similarities > threshold).item()

        return SearchResultList(
            results=[
                SearchResult(text="YES" if is_any_doc_relevant else "NO", metadata={})
            ],
            metadata={},
        )

    async def _generate_final_answer(
        self,
        message: Message,
        documents: SearchResultList,
        llm: LLMClient,
        tracker: DialogueStateTracker,
    ) -> SearchResultList:
        input = {
            "current_conversation": tracker_as_readable_transcript(tracker),
            "relevant_documents": documents,
            "user_message": message.get(TEXT),
        }
        prompt = self.render_prompt(input)
        response = await self._invoke_llm(prompt, llm)
        response_text = response.choices[0] if response else ""
        search_result = SearchResult(text=response_text, metadata={})
        results = SearchResultList(
            results=[search_result],
            metadata={},
        )
        return results
