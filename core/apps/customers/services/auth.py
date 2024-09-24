from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomersService
from core.apps.customers.services.sendors import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomersService
    codes_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, phone: str, username: str): ...

    @abstractmethod
    def confirm(self, phone: str, code: str): ...


class AuthService(BaseAuthService):
    def authorize(self, phone: str, username: str):
        customer = self.customer_service.get_or_create(phone, username)
        code = self.codes_service.generate_code(customer)
        self.sender_service.send_code(customer, code)

    def confirm(self, phone: str, code: str):
        customer = self.customer_service.get(phone)
        self.codes_service.validate_code(customer, code)
        return self.customer_service.generate_token(customer)
