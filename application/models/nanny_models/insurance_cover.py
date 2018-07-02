from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .base import ApiCalls
from .nanny_application import NannyApplication


class InsuranceCover(models.Model):
    """
    Model for INSURANCE_COVER table
    """
    objects = models.Manager()
    api = ApiCalls("insurance-cover", 'insurance_cover_id')
    insurance_cover_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    public_liability = models.NullBooleanField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'INSURANCE_COVER'


class InsuranceCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCover
        fields = '__all__'

