from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from presspulse.users.models import Profile

from .serializers import ProfileSerializer


class ProfileViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, email):
        serializer = ProfileSerializer(Profile.objects.get(email=email))
        return Response(status=status.HTTP_200_OK, data=serializer.data)
