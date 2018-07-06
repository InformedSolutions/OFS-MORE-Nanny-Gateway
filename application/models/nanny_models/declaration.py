from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .base import ApiCalls
from .nanny_application import NannyApplication


class Declaration(models.Model):
    """
    Model for DECLARATION table
    """
    objects = models.Manager()
    api = ApiCalls("declaration", 'declaration_id')
    declaration_id = models.UUIDField(primary_key=True, default=uuid4())
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    register_rules = models.NullBooleanField(blank=True, null=True)
    share_information = models.NullBooleanField(blank=True, null=True)
    information_correct = models.NullBooleanField(blank=True, null=True)
    notify_information_change = models.NullBooleanField(blank=True, null=True)


class DeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaration
        fields = '__all__'

