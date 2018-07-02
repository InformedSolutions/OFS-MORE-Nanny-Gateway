from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .base import ApiCalls
from .nanny_application import NannyApplication


class DbsCheck(models.Model):
    """
    Model for DBS_CHECK table
    """
    objects = models.Manager()
    api = ApiCalls("dbs-check", 'dbs_id')
    dbs_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    dbs_number = models.CharField(max_length=100)
    convictions = models.NullBooleanField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'DBS_CHECK'


class DbsCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbsCheck
        fields = '__all__'

