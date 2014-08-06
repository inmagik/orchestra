from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from orchestra_core.utils import generate_uuid

# Create your models here.

class Workflow(models.Model):
    
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    oid = models.CharField(max_length=200, null=True, blank=True, default=generate_uuid)


class Operation(models.Model):
    """
    A model to represent a single Operation
    """
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    task = models.CharField(max_length=200, null=True, blank=True)
    args = JSONField(null=True, blank=True)

    partials = JSONField(null=True, blank=True)
    oid = models.CharField(max_length=200, null=True, blank=True)

    workflow = models.ForeignKey(Workflow, null=True, blank=True, related_name="operations")



    








