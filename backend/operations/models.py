from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Create your models here.


class Operation(models.Model):
    """
    A model to represent a single Operation
    """
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    task = models.CharField(max_length=200, null=True, blank=True)
    args = JSONField(null=True, blank=True)