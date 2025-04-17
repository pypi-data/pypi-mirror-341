from typing import Any, Dict, Optional

from rasa.core.information_retrieval import SearchResultList
from rasa.document_retrieval.knowledge_base_connectors.knowledge_base_connector import (
    KnowledgeBaseConnector,
)
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.core.trackers import DialogueStateTracker


class APIConnector(KnowledgeBaseConnector):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config

    @classmethod
    def load(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> "APIConnector":
        # TODO implement
        return APIConnector(config)

    async def retrieve_documents(
        self,
        search_query: str,
        k: int,
        threshold: float,
        tracker: Optional[DialogueStateTracker],
    ) -> Optional[SearchResultList]:
        # TODO implement
        return SearchResultList(results=[], metadata={})

    def connect_or_raise(self) -> None:
        # TODO implement
        return None
