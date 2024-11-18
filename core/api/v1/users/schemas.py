from pydantic import BaseModel
from datetime import datetime

from core.apps.customers.entities import CustomerEntity


class UserSchema(BaseModel):
    username: str
    phone: str
    bio: str
    role: str

    @staticmethod
    def from_entity(entity: CustomerEntity) -> "UserSchema":
        return UserSchema(
            username=entity.username,
            phone=entity.phone,
            bio=entity.bio,
            role=entity.role,
        )
