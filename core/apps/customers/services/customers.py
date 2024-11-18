from abc import ABC, abstractmethod
from uuid import uuid4

from django.db.models import Q

from core.api.filters import PaginationIn
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.customers import CustomerTokenInvalid
from core.apps.customers.filters import UserFilters
from core.apps.customers.models import Customer as CustomerDTO


class BaseCustomersService(ABC):
    @abstractmethod
    def get_or_create(self, phone: str, username: str) -> CustomerEntity: ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity): ...

    @abstractmethod
    def get(self, phone: str) -> CustomerEntity: ...

    @abstractmethod
    def get_by_token(self, token: str) -> CustomerEntity: ...

    @abstractmethod
    def get_all_users(
        self, filters: UserFilters, pagination: PaginationIn
    ) -> list[CustomerEntity]: ...


class ORMCustomerService(BaseCustomersService):
    def get_or_create(self, phone: str, username: str) -> CustomerEntity:
        user_dto, _ = CustomerDTO.objects.get_or_create(phone=phone, username=username)
        return user_dto.to_entity()

    def get(self, phone: str) -> CustomerEntity:
        user_dto = CustomerDTO.objects.get(phone=phone)
        return user_dto.to_entity()

    def generate_token(self, customer: CustomerEntity):
        new_token = str(uuid4())
        CustomerDTO.objects.filter(phone=customer.phone).update(token=new_token)
        return new_token

    def get_by_token(self, token: str) -> CustomerEntity:
        try:
            user_dto = CustomerDTO.objects.get(token=token)
        except CustomerDTO.DoesNotExist:
            raise CustomerTokenInvalid(token=token)

        return user_dto.to_entity()

    def _build_user_query(self, filters: UserFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query = Q(username__icontains=filters.search)
        return query

    def get_all_users(
        self, filters: UserFilters, pagination: PaginationIn
    ) -> list[CustomerEntity]:
        query = self._build_user_query(filters)
        qs = CustomerDTO.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]
        return [user.to_entity() for user in qs]
