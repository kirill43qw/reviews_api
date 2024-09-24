from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from core.apps.customers.entities import CustomerEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: CustomerEntity, code: str) -> None: ...


class DummySenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f"Code to user: {customer}, send: {code}")


class PushSenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f"senf push notification with {code} fcm_token from {customer.username}")


@dataclass
class TelegramSenderService(BaseSenderService):
    secret_key: str

    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(
            f"Code to telegram bot phone: {customer.phone}, send: {code}, and {self.secret_key} "
        )


@dataclass
class ComposeSenderService(BaseSenderService):
    sender_services: Iterable[BaseSenderService]

    def send_code(self, customer: CustomerEntity, code: str) -> None:
        for service in self.sender_services:
            service.send_code(customer=customer, code=code)
