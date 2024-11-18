from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.common.elasticsearch import ElasticClient
from core.apps.reviews.entities.titles import TitleEntity


@dataclass
class BaseTitleSearchService(ABC):
    @abstractmethod
    def upsert_title(self, title: TitleEntity): ...

    @abstractmethod
    def delete_title(self, title_id: id): ...


@dataclass
class ElasticTitleSearchService(BaseTitleSearchService):
    client: ElasticClient
    index_name: str

    @staticmethod
    def _build_as_document(title: TitleEntity):
        return {
            "id": title.id,
            "title": title.title,
            "description": title.description,
            # "category": title.category.name if title.category else None,
            # "genre": title.genre.name if title.genre else None,
        }

    def upsert_title(self, title: TitleEntity):
        self.client.upsert_index(
            index=self.index_name,
            document_id=title.id,
            document=self._build_as_document(title),
        )

    def delete_title(self, title_id: int):
        self.client.delete_doc(index=self.index_name, document_id=title_id)
