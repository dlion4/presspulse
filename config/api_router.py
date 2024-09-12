from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from presspulse.users.api.views import ProfileViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("profiles", ProfileViewSet)


app_name = "api"
urlpatterns = router.urls
