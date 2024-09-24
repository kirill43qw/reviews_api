from datetime import datetime
from pydantic import BaseModel

from core.apps.reviews.entities import TitleEntity


class TitleSchema(BaseModel):
    id: int
    title: str
    description: str
    rating: int
    year: int

    @staticmethod
    def from_entity(entity: TitleEntity) -> "TitleSchema":
        return TitleSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            rating=entity.rating,
            year=entity.year,
        )
