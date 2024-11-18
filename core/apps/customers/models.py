from uuid import uuid4

from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity


class Customer(TimedBaseModel):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE = ((USER, "user"), (ADMIN, "admin"), (MODERATOR, "moderator"))

    username = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )
    phone = models.CharField(
        verbose_name="Phone Number",
        max_length=20,
        unique=True,
    )
    token = models.CharField(
        verbose_name="User Token",
        max_length=255,
        default=uuid4,
        unique=True,
    )
    bio = models.CharField(
        max_length=200,
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default=USER,
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            id=self.id,
            username=self.username,
            phone=self.phone,
            bio=self.phone,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
