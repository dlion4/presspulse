from typing import Any

from django.shortcuts import render
from django.views.generic import TemplateView

from website.main.posts.models import Category
from website.main.posts.models import Tag


# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["categories"] = Category.objects.all().order_by("?")[:4]
        return context

