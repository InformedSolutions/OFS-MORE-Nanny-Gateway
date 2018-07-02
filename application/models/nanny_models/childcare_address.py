from uuid import uuid4

from rest_framework import serializers
from .base import ApiCalls
from django.db import models
from .nanny_application import NannyApplication


class ChildcareAddress(models.Model):
    """
        Model for Nanny Application table
    """
    # Managers
    objects = models.Manager()
    api = ApiCalls("childcare-address", "childcare_address_id")

    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    date_created = models.DateTimeField(blank=True, null=True)
    childcare_address_id = models.UUIDField(primary_key=True, default=uuid4)
    street_line1 = models.CharField(max_length=100, blank=True, null=True)
    street_line2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def get_id(cls, childcare_address_id):
        return cls.objects.get(pk=childcare_address_id)

    class Meta:
        db_table = 'CHILDCARE_ADDRESS'


class ChildcareAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildcareAddress
        fields = '__all__'
