from django.contrib import admin

from core.apps.reviews.models import Category, Genre, Title, Review
from core.apps.reviews.models.comments import Comment


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
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
    list_display = ("id", "text", "rating", "title_id")
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "review", "author_id")
