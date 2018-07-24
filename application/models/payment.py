"""
Entity definition for payments made in relation to an application
"""
from uuid import uuid4

from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class Payment(models.Model):
    """
    A model for tracking the capture and processing of payments
    """
    objects = models.Manager()
    api = ApiCalls("payment", "application_id")

    # Unique payment record identifier
    payment_id = models.UUIDField(primary_key=True, default=uuid4)

    # Foreign Key relation to an application
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')

    # Payment reference which adheres to a format of
    # MORE:<<Application reference>>:<<Timestamp of lodged payment>>
    payment_reference = models.CharField(max_length=29, blank=False, null=False)

    # Flag to track whether a payment request has been issued to Worldpay
    payment_submitted = models.BooleanField(default=False)

    # Flag to track whether a payment has been marked as Authorised by Worldpay
    # i.e. the funds have been debited from the users account
    payment_authorised = models.BooleanField(default=False)

    class Meta:
        db_table = 'PAYMENT'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

