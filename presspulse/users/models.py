

from django.db import models
from django.db.models import EmailField


class Profile(models.Model):
    email = EmailField(max_length=1000, unique=True)

    def __str__(self):
        return self.email

