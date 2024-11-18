from django.contrib import admin

from core.apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "token", "phone", "role")
    search_fields = ("username",)
