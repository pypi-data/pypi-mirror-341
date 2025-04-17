import importlib.resources
from enum import Enum
from typing import Any, Dict, Optional

import structlog
from jinja2 import Template

import rasa.shared.utils.io
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
from rasa.shared.utils.health_check.llm_health_check_mixin import (
    LLMHealthCheckMixin,
)
from rasa.shared.utils.llm import (
    AI,
    DEFAULT_OPENAI_GENERATE_MODEL_NAME,
    DEFAULT_OPENAI_MAX_GENERATED_TOKENS,
    USER,
    get_prompt_template,
    llm_factory,
    resolve_model_client_config,
    sanitize_message_for_prompt,
    tracker_as_readable_transcript,
)

QUERY_REWRITER_PROMPT_FILE_NAME = "query_rewriter_prompt_template.jinja2"
MAX_TURNS = "max_turns"
DEFAULT_LLM_CONFIG = {
    PROVIDER_CONFIG_KEY: OPENAI_PROVIDER,
    MODEL_CONFIG_KEY: DEFAULT_OPENAI_GENERATE_MODEL_NAME,
    "temperature": 0.3,
    "max_tokens": DEFAULT_OPENAI_MAX_GENERATED_TOKENS,
    TIMEOUT_CONFIG_KEY: 5,
}
DEFAULT_QUERY_REWRITER_PROMPT_TEMPLATE = importlib.resources.read_text(
    "rasa.document_retrieval",
    "query_rewriter_prompt_template.jinja2",
)

TYPE_CONFIG_KEY = "type"

structlogger = structlog.get_logger()


class QueryRewritingType(Enum):
    PLAIN = "PLAIN"
    CONCATENATED_TURNS = "CONCATENATED_TURNS"
    REPHRASE = "REPHRASE"
    KEYWORD_EXTRACTION = "KEYWORD_EXTRACTION"

    def __str__(self) -> str:
        return self.value


class QueryRewriter(LLMHealthCheckMixin):
    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """The default config for the query rewriter."""
        return {
            TYPE_CONFIG_KEY: QueryRewritingType.PLAIN,
            MAX_TURNS: 0,
            LLM_CONFIG_KEY: DEFAULT_LLM_CONFIG,
            PROMPT_TEMPLATE_CONFIG_KEY: DEFAULT_QUERY_REWRITER_PROMPT_TEMPLATE,
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
            self.config.get(LLM_CONFIG_KEY), QueryRewriter.__name__
        )
        self.prompt_template = prompt_template or get_prompt_template(
            config.get(PROMPT_TEMPLATE_CONFIG_KEY),
            DEFAULT_QUERY_REWRITER_PROMPT_TEMPLATE,
        )

        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def load(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> "QueryRewriter":
        """Load query rewriter."""
        llm_config = resolve_model_client_config(config.get(LLM_CONFIG_KEY, {}))
        perform_llm_health_check(
            llm_config,
            DEFAULT_LLM_CONFIG,
            "query_rewriter.load",
            QueryRewriter.__name__,
        )

        # load prompt template
        prompt_template = None
        try:
            with model_storage.read_from(resource) as path:
                prompt_template = rasa.shared.utils.io.read_file(
                    path / QUERY_REWRITER_PROMPT_FILE_NAME
                )
        except (FileNotFoundError, FileIOException) as e:
            structlogger.warning(
                "query_rewriter.load_prompt_template.failed",
                error=e,
                resource=resource.name,
            )

        return QueryRewriter(config, model_storage, resource, prompt_template)

    def persist(self) -> None:
        with self._model_storage.write_to(self._resource) as path:
            rasa.shared.utils.io.write_text_file(
                self.prompt_template, path / QUERY_REWRITER_PROMPT_FILE_NAME
            )

    @staticmethod
    def _concatenate_turns(
        message: Message, tracker: DialogueStateTracker, max_turns: int
    ) -> str:
        transcript = tracker_as_readable_transcript(tracker, max_turns=max_turns)
        transcript += "\nUSER: " + message.get(TEXT)
        return transcript

    @staticmethod
    async def _invoke_llm(prompt: str, llm: LLMClient) -> Optional[LLMResponse]:
        try:
            return await llm.acompletion(prompt)
        except Exception as e:
            # unfortunately, langchain does not wrap LLM exceptions which means
            # we have to catch all exceptions here
            structlogger.error("query_rewriter.llm.error", error=e)
            raise ProviderClientAPIException(
                message="LLM call exception", original_exception=e
            )

    async def _rephrase_message(
        self, message: Message, tracker: DialogueStateTracker, max_turns: int = 5
    ) -> str:
        llm = llm_factory(self.config.get(LLM_CONFIG_KEY), DEFAULT_LLM_CONFIG)

        transcript = tracker_as_readable_transcript(
            tracker, max_turns=max_turns, ai_prefix="ASSISTANT"
        )

        inputs = {
            "conversation": transcript,
            "user_message": message.get(TEXT),
        }

        prompt = Template(self.prompt_template).render(**inputs)
        llm_response = await self._invoke_llm(prompt, llm)
        llm_response = LLMResponse.ensure_llm_response(llm_response)

        return llm_response.choices[0]

    @staticmethod
    def _keyword_extraction(
        message: Message, tracker: DialogueStateTracker, max_turns: int = 5
    ) -> str:
        import spacy

        nlp = spacy.load("en_core_web_md")

        transcript = tracker_as_readable_transcript(tracker, max_turns=max_turns)
        transcript = transcript.replace(USER, "")
        transcript = transcript.replace(AI, "")

        doc = nlp(transcript)

        keywords = set()
        for token in doc:
            # Extract nouns and proper nouns
            if token.pos_ in ["NOUN", "PROPN"]:
                keywords.add(token.lemma_)

        for ent in doc.ents:
            # Add named entities as keywords
            keywords.add(ent.text)

        # Remove stop words and punctuation
        keywords = {
            word
            for word in keywords
            if word.lower() not in nlp.Defaults.stop_words and word.isalpha()
        }

        if keywords:
            return message.get(TEXT) + " " + " ".join(keywords)
        else:
            return message.get(TEXT)

    async def prepare_search_query(
        self, message: Message, tracker: DialogueStateTracker
    ) -> str:
        query_rewriting_type = self.config[TYPE_CONFIG_KEY]
        max_turns: int = self.config[MAX_TURNS]

        query: str

        if query_rewriting_type == QueryRewritingType.CONCATENATED_TURNS.value:
            query = self._concatenate_turns(message, tracker, max_turns)
        elif query_rewriting_type == QueryRewritingType.KEYWORD_EXTRACTION.value:
            query = self._keyword_extraction(message, tracker, max_turns)
        elif query_rewriting_type == QueryRewritingType.REPHRASE.value:
            query = await self._rephrase_message(message, tracker, max_turns)
        elif query_rewriting_type == QueryRewritingType.PLAIN.value:
            query = message.get(TEXT)
        else:
            raise ValueError(f"Invalid query rewriting type: {query_rewriting_type}")

        return sanitize_message_for_prompt(query)
