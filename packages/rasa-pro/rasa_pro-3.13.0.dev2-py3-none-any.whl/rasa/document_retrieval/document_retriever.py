from __future__ import annotations

import datetime
import time
import uuid
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Text

import structlog

from rasa.core.information_retrieval.faiss import FAISS_Store
from rasa.dialogue_understanding.utils import add_prompt_to_message_parse_data
from rasa.document_retrieval.constants import (
    CONNECTOR_CONFIG_KEY,
    DEFAULT_K,
    DEFAULT_THRESHOLD,
    K_CONFIG_KEY,
    POST_PROCESSED_DOCUMENTS_KEY,
    POST_PROCESSING_CONFIG_KEY,
    QUERY_REWRITING_CONFIG_KEY,
    RETRIEVED_DOCUMENTS_KEY,
    SEARCH_QUERY_KEY,
    SOURCE_PROPERTY,
    THRESHOLD_CONFIG_KEY,
    USE_LLM_PROPERTY,
    VECTOR_STORE_CONFIG_KEY,
    VECTOR_STORE_TYPE_CONFIG_KEY,
)
from rasa.document_retrieval.document_post_processor import DocumentPostProcessor
from rasa.document_retrieval.knowledge_base_connectors.api_connector import APIConnector
from rasa.document_retrieval.knowledge_base_connectors.knowledge_base_connector import (
    KnowledgeBaseConnector,
)
from rasa.document_retrieval.knowledge_base_connectors.vector_store_connector import (
    DEFAULT_EMBEDDINGS_CONFIG,
    VectorStoreConnector,
    VectorStoreType,
)
from rasa.document_retrieval.query_rewriter import QueryRewriter
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.constants import (
    EMBEDDINGS_CONFIG_KEY,
)
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.providers.embedding._langchain_embedding_client_adapter import (
    _LangchainEmbeddingClientAdapter,
)
from rasa.shared.providers.llm.llm_response import LLMResponse
from rasa.shared.utils.llm import (
    embedder_factory,
    resolve_model_client_config,
)

if TYPE_CHECKING:
    from langchain.schema.embeddings import Embeddings

structlogger = structlog.get_logger()


class ConnectorType(Enum):
    API = "API"
    VECTOR_STORE = "VECTOR_STORE"

    def __str__(self) -> str:
        return self.value


@DefaultV1Recipe.register(
    [
        DefaultV1Recipe.ComponentType.COEXISTENCE_ROUTER,
    ],
    is_trainable=True,
)
class DocumentRetriever(GraphComponent):
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """The component's default config (see parent class for full docstring)."""
        return {
            THRESHOLD_CONFIG_KEY: DEFAULT_THRESHOLD,
            K_CONFIG_KEY: DEFAULT_K,
            CONNECTOR_CONFIG_KEY: ConnectorType.VECTOR_STORE.value,
            EMBEDDINGS_CONFIG_KEY: DEFAULT_EMBEDDINGS_CONFIG,
            VECTOR_STORE_CONFIG_KEY: {
                VECTOR_STORE_TYPE_CONFIG_KEY: VectorStoreType.FAISS.value,
            },
        }

    def __init__(
        self,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        query_rewriter: Optional[QueryRewriter] = None,
        document_post_processor: Optional[DocumentPostProcessor] = None,
        knowledge_base_connector: Optional[KnowledgeBaseConnector] = None,
    ) -> None:
        self.config = {**self.get_default_config(), **config}
        self.config[EMBEDDINGS_CONFIG_KEY] = resolve_model_client_config(
            self.config.get(EMBEDDINGS_CONFIG_KEY), DocumentRetriever.__name__
        )

        self._model_storage = model_storage
        self._resource = resource

        # Disable query rewriting and post processing if they are not set
        query_rewriting_config = config.get(
            QUERY_REWRITING_CONFIG_KEY, {"type": "PLAIN"}
        )
        post_processing_config = config.get(
            POST_PROCESSING_CONFIG_KEY, {"type": "PLAIN"}
        )

        self.query_rewriter = query_rewriter or QueryRewriter(
            query_rewriting_config, model_storage, resource
        )
        self.document_post_processor = document_post_processor or DocumentPostProcessor(
            post_processing_config, model_storage, resource
        )
        self.knowledge_base_connector = (
            knowledge_base_connector or self.initialize_knowledge_base_connector()
        )

        self.use_llm = self.config.get(USE_LLM_PROPERTY, False)

    def persist(self) -> None:
        """Persist this component to disk for future loading."""
        self.query_rewriter.persist()
        self.document_post_processor.persist()

    @classmethod
    def _create_plain_embedder(cls, config: Dict[Text, Any]) -> "Embeddings":
        """Creates an embedder based on the given configuration.

        Returns:
        The embedder.
        """
        # Copy the config so original config is not modified
        config = config.copy()
        # Resolve config and instantiate the embedding client
        config[EMBEDDINGS_CONFIG_KEY] = resolve_model_client_config(
            config.get(EMBEDDINGS_CONFIG_KEY), DocumentRetriever.__name__
        )
        client = embedder_factory(
            config.get(EMBEDDINGS_CONFIG_KEY), DEFAULT_EMBEDDINGS_CONFIG
        )
        # Wrap the embedding client in the adapter
        return _LangchainEmbeddingClientAdapter(client)

    def train(self, training_data: TrainingData) -> Resource:
        """Train the document retriever on a data set."""
        store_type = self.config.get(VECTOR_STORE_CONFIG_KEY, {}).get(
            VECTOR_STORE_TYPE_CONFIG_KEY
        )
        if store_type == VectorStoreType.FAISS.value:
            structlogger.info("document_retriever.train.faiss")
            embeddings = self._create_plain_embedder(self.config)
            with self._model_storage.write_to(self._resource) as path:
                self.vector_store = FAISS_Store(
                    docs_folder=self.config.get(VECTOR_STORE_CONFIG_KEY, {}).get(
                        SOURCE_PROPERTY
                    ),
                    embeddings=embeddings,
                    index_path=path,
                    create_index=True,
                    use_llm=self.use_llm,
                )
        self.persist()
        return self._resource

    @classmethod
    def load(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> "DocumentRetriever":
        """Loads trained component (see parent class for full docstring)."""
        # Load query rewriter and document post processor

        # Disable query rewriting and post processing if they are not set
        query_rewriting_config = config.get(
            QUERY_REWRITING_CONFIG_KEY, {"type": "PLAIN"}
        )
        post_processing_config = config.get(
            POST_PROCESSING_CONFIG_KEY, {"type": "PLAIN"}
        )

        query_rewriter = QueryRewriter.load(
            query_rewriting_config, model_storage, resource
        )
        document_post_processor = DocumentPostProcessor.load(
            post_processing_config, model_storage, resource
        )

        connector_type = config.get(CONNECTOR_CONFIG_KEY)
        knowledge_base_connector: KnowledgeBaseConnector

        if connector_type == ConnectorType.VECTOR_STORE.value:
            knowledge_base_connector = VectorStoreConnector.load(
                config, model_storage, resource
            )
        elif connector_type == ConnectorType.API.value:
            knowledge_base_connector = APIConnector.load(
                config, model_storage, resource
            )
        else:
            raise ValueError(f"Invalid knowledge base connector: {connector_type}")

        return cls(
            config,
            model_storage,
            resource,
            query_rewriter,
            document_post_processor,
            knowledge_base_connector,
        )

    @classmethod
    def create(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> DocumentRetriever:
        """Creates component (see parent class for full docstring)."""
        return cls(config, model_storage, resource)

    def initialize_knowledge_base_connector(self) -> KnowledgeBaseConnector:
        connector_type = self.config.get(CONNECTOR_CONFIG_KEY)

        if connector_type == ConnectorType.VECTOR_STORE.value:
            return VectorStoreConnector(
                self.config,
                self._model_storage,
                self._resource,
            )
        elif connector_type == ConnectorType.API.value:
            return APIConnector(self.config)
        else:
            raise ValueError(f"Invalid knowledge base connector: {type}")

    async def process(
        self,
        messages: List[Message],
        tracker: Optional[DialogueStateTracker] = None,
    ) -> List[Message]:
        """Process a list of messages."""
        self.knowledge_base_connector.connect_or_raise()

        for message in messages:
            start = time.time()

            # Prepare search query
            search_query = await self.query_rewriter.prepare_search_query(
                message, tracker
            )
            message.set(
                SEARCH_QUERY_KEY,
                search_query,
                add_to_output=True,
            )

            # Retrieve documents
            search_result = await self.knowledge_base_connector.retrieve_documents(
                search_query,
                self.config[K_CONFIG_KEY] or DEFAULT_K,
                self.config[THRESHOLD_CONFIG_KEY] or DEFAULT_THRESHOLD,
                tracker,
            )

            if search_result is None:
                message.set(
                    RETRIEVED_DOCUMENTS_KEY,
                    [],
                    add_to_output=True,
                )
                message.set(
                    POST_PROCESSED_DOCUMENTS_KEY,
                    [],
                    add_to_output=True,
                )
                continue

            message.set(
                RETRIEVED_DOCUMENTS_KEY,
                search_result.to_dict(),
                add_to_output=True,
            )

            # Post process documents
            final_search_result = await self.document_post_processor.process_documents(
                message, search_query, search_result, tracker
            )
            message.set(
                POST_PROCESSED_DOCUMENTS_KEY,
                final_search_result.to_dict(),
                add_to_output=True,
            )

            structlogger.debug(
                "document_retriever.process",
                search_query=search_query,
                search_result=search_result.to_dict(),
                final_search_result=final_search_result.to_dict(),
            )

            end = time.time()
            add_prompt_to_message_parse_data(
                message,
                DocumentRetriever.__name__,
                "document_retriever_process",
                user_prompt="Dummy prompt for document retriever process.",
                llm_response=LLMResponse(
                    id=str(uuid.uuid4()),
                    choices=[
                        f"search_query: {search_query}\n"
                        f"retrieved_documents: {search_result.to_dict()}\n"
                        f"post_processed_documents: {final_search_result.to_dict()}",
                    ],
                    created=int(datetime.datetime.now().timestamp()),
                    latency=end - start,
                ),
            )

        return messages
