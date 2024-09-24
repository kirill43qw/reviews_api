from django.contrib import admin

from core.apps.reviews.models import Category, Genre, Title, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year", "rating")
    inlines = (ReviewInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "rating")
