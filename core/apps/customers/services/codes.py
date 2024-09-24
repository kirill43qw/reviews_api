import random
from abc import ABC, abstractmethod

from django.core.cache import cache

from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.codes import (
    CodeNotFoundException,
    CodesNotEqualException,
)


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, customer: CustomerEntity) -> str: ...

    @abstractmethod
    def validate_code(self, customer: CustomerEntity, code: str) -> None: ...


class DjangoCacheService(BaseCodeService):
    def generate_code(self, customer: CustomerEntity) -> str:
        code = str(random.randint(100000, 999999))
        cache.set(customer.phone, code)
        return code

    def validate_code(self, customer: CustomerEntity, code: str) -> None:
        cached_code = cache.get(customer.phone)

        if code is None:
            raise CodeNotFoundException(code=code)
        if cached_code != code:
            raise CodesNotEqualException(
                code=code,
                cached_code=cached_code,
                customer_phone=customer.phone,
            )
