from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from rasa.core.information_retrieval import SearchResultList
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.core.trackers import DialogueStateTracker


class KnowledgeBaseConnector(ABC):
    @abstractmethod
    def connect_or_raise(self) -> None:
        pass

    @abstractmethod
    async def retrieve_documents(
        self,
        search_query: str,
        k: int,
        threshold: float,
        tracker: Optional[DialogueStateTracker],
    ) -> Optional[SearchResultList]:
        pass

    @classmethod
    @abstractmethod
    def load(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        **kwargs: Any,
    ) -> "KnowledgeBaseConnector":
        pass
