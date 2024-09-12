from rest_framework import serializers

from presspulse.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer[Profile]):
    class Meta:
        model = Profile
        fields = ["email", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:profile-detail", "lookup_field": "pk"},
        }
