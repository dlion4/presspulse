from typing import Any

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from website.main.posts.models import Category
from website.main.posts.models import Tag


class HomeCategoryDetailView(TemplateView):
    template_name = "category.html"
    model = Category
    def get_category(self, **kwargs):
        return get_object_or_404(Category, slug=kwargs.get("slug"))
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category(**kwargs)
        context["categories"] = Category.objects.all().order_by("?")[:4]
        context["complete_categories"] = Category.objects.exclude(
            pk=self.get_category(**kwargs).pk).all()
        context["tags"] = Tag.objects.all()
        return context
