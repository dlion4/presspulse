from django.urls import include
from django.urls import path

from .views import index

app_name = "university"

urlpatterns = [
    path("", index),
]
