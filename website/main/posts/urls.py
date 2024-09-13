from django.urls import include
from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path("<slug>/", views.HomeCategoryDetailView.as_view(), name="category_detail"),
]
