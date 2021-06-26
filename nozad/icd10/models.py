from django.db import models
from django.utils import timezone


# Create your models here.

class Icd10(models.Model):

    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    nationalcode = models.CharField(max_length=10, null=False, blank=False)
    # nationalcode = models.IntegerField(null=False, blank=False)
    doctorname = models.CharField(max_length=200, null=False, blank=False)
    # explanation = models.TextField(null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    codes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)