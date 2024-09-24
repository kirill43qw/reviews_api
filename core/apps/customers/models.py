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

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username

    def to_entity(self) -> CustomerEntity:
        return CustomerEntity(
            phone=self.phone,
            username=self.username,
            created_at=self.created_at,
            id=self.pk,
        )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
