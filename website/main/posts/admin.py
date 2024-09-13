from django.contrib import admin

from .models import Category
from .models import Tag


# Register your models here.
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name", )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name", )}
