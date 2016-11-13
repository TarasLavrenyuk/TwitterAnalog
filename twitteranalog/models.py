from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Extra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    continent = models.CharField(max_length=15)