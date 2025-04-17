import copy
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional

import structlog

from rasa.core.information_retrieval import (
    InformationRetrieval,
    InformationRetrievalException,
    SearchResultList,
    create_from_endpoint_config,
)
from rasa.core.information_retrieval.faiss import FAISS_Store
from rasa.document_retrieval.constants import (
    DEFAULT_EMBEDDINGS_CONFIG,
    DEFAULT_VECTOR_STORE,
    DEFAULT_VECTOR_STORE_TYPE,
    VECTOR_STORE_CONFIG_KEY,
    VECTOR_STORE_TYPE_CONFIG_KEY,
)
from rasa.document_retrieval.knowledge_base_connectors.knowledge_base_connector import (
    KnowledgeBaseConnector,
)
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.constants import EMBEDDINGS_CONFIG_KEY
from rasa.shared.core.trackers import DialogueStateTracker, EventVerbosity
from rasa.shared.exceptions import RasaException
from rasa.shared.providers.embedding._langchain_embedding_client_adapter import (
    _LangchainEmbeddingClientAdapter,
)
from rasa.shared.utils.health_check.embeddings_health_check_mixin import (
    EmbeddingsHealthCheckMixin,
)
from rasa.shared.utils.health_check.health_check import perform_embeddings_health_check
from rasa.shared.utils.llm import embedder_factory, resolve_model_client_config

if TYPE_CHECKING:
    from langchain.schema.embeddings import Embeddings


structlogger = structlog.get_logger()


class VectorStoreConnectionError(RasaException):
    """Exception raised for errors in connecting to the vector store."""


class VectorStoreConfigurationError(RasaException):
    """Exception raised for errors in vector store configuration."""


class VectorStoreType(Enum):
    FAISS = "FAISS"
    QDRANT = "QDRANT"
    MILVUS = "MILVUS"

    def __str__(self) -> str:
        return self.value


class VectorStoreConnector(KnowledgeBaseConnector, EmbeddingsHealthCheckMixin):
    def __init__(
        self,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        vector_store: Optional[InformationRetrieval] = None,
    ) -> None:
        self.config = config
        self.vector_store_type = config.get(VECTOR_STORE_CONFIG_KEY, {}).get(
            VECTOR_STORE_TYPE_CONFIG_KEY
        )

        # Vector store object and configuration
        self.vector_store = vector_store
        self.vector_store_config = self.config.get(
            VECTOR_STORE_CONFIG_KEY, DEFAULT_VECTOR_STORE
        )

        # Embeddings configuration for encoding the search query
        self.embeddings_config = (
            self.config[EMBEDDINGS_CONFIG_KEY] or DEFAULT_EMBEDDINGS_CONFIG
        )

        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def _create_plain_embedder(cls, config: Dict[str, Any]) -> "Embeddings":
        """Creates an embedder based on the given configuration.

        Returns:
        The embedder.
        """
        # Copy the config so original config is not modified
        config = copy.deepcopy(config)
        # Resolve config and instantiate the embedding client
        config[EMBEDDINGS_CONFIG_KEY] = resolve_model_client_config(
            config.get(EMBEDDINGS_CONFIG_KEY), VectorStoreConnector.__name__
        )
        client = embedder_factory(
            config.get(EMBEDDINGS_CONFIG_KEY), DEFAULT_EMBEDDINGS_CONFIG
        )
        # Wrap the embedding client in the adapter
        return _LangchainEmbeddingClientAdapter(client)

    @classmethod
    def load(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> "VectorStoreConnector":
        # Perform health check on the resolved embeddings client config
        embedding_config = resolve_model_client_config(
            config.get(EMBEDDINGS_CONFIG_KEY, {})
        )
        perform_embeddings_health_check(
            embedding_config,
            DEFAULT_EMBEDDINGS_CONFIG,
            "vector_store_connector.load",
            VectorStoreConnector.__name__,
        )

        store_type = config.get(VECTOR_STORE_CONFIG_KEY, {}).get(
            VECTOR_STORE_TYPE_CONFIG_KEY
        )
        embeddings = cls._create_plain_embedder(config)

        structlogger.info("vector_store_connector.load", config=config)
        if store_type == VectorStoreType.FAISS.value:
            # if a vector store is not specified,
            # default to using FAISS with the index stored in the model
            # TODO figure out a way to get path without context manager
            with model_storage.read_from(resource) as path:
                vector_store = FAISS_Store(
                    embeddings=embeddings,
                    index_path=path,
                    docs_folder=None,
                    create_index=False,
                )
        else:
            vector_store = create_from_endpoint_config(
                config_type=store_type,
                embeddings=embeddings,
            )  # type: ignore

        return cls(
            config=config,
            model_storage=model_storage,
            resource=resource,
            vector_store=vector_store,
        )

    def connect_or_raise(self) -> None:
        """Connects to the vector store or raises an exception.

        Raise exceptions for the following cases:
        - The configuration is not specified
        - Unable to connect to the vector store

        Args:
            endpoints: Endpoints configuration.
        """
        if self.vector_store_type == VectorStoreType.FAISS.value:
            return
        from rasa.core.utils import AvailableEndpoints

        endpoints = AvailableEndpoints.get_instance()

        config = endpoints.vector_store if endpoints else None
        store_type = self.config.get(VECTOR_STORE_CONFIG_KEY, {}).get(
            VECTOR_STORE_TYPE_CONFIG_KEY
        )

        if config is None and store_type != DEFAULT_VECTOR_STORE_TYPE:
            structlogger.error("vector_store_connector._connect_or_raise.no_config")
            raise VectorStoreConfigurationError(
                """No vector store specified. Please specify a vector
                store in the endpoints configuration."""
            )
        try:
            self.vector_store.connect(config)  # type: ignore
        except Exception as e:
            structlogger.error(
                "vector_store_connector._connect_or_raise.connect_error",
                error=e,
                config=config,
            )
            raise VectorStoreConnectionError(
                f"Unable to connect to the vector store. Error: {e}"
            )

    async def retrieve_documents(
        self,
        search_query: str,
        k: int,
        threshold: float,
        tracker: Optional[DialogueStateTracker],
    ) -> Optional[SearchResultList]:
        if self.vector_store is None:
            return None

        try:
            self.connect_or_raise()
        except (VectorStoreConfigurationError, VectorStoreConnectionError) as e:
            structlogger.error("vector_store_connector.connection_error", error=e)
            return None

        if tracker is not None:
            tracker_state = tracker.current_state(EventVerbosity.AFTER_RESTART)
        else:
            tracker_state = {}

        try:
            return await self.vector_store.search(
                query=search_query,
                threshold=threshold,
                tracker_state=tracker_state,
                k=k,
            )
        except InformationRetrievalException as e:
            structlogger.error("vector_store.search_error", error=e)
            return None
