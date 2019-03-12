from uuid import uuid4

from rest_framework import serializers
from django.db import models

from django.db import models


from application.models import NannyApplication

class NannyPreviousRegistrationDetails(models.Model):
    """
    Model for PREVIOUS_REGISTRATION_DETAILS table
    """

    objects = models.Manager()

    previous_registration_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    previous_registration = models.NullBooleanField(blank=True, null=True)
    individual_id = models.IntegerField(default=0, null=True, blank=True)
    five_years_in_UK = models.NullBooleanField(blank=True, null=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        :return: tuple of fields which needs update tracking when application is returned
        """
        return (
            'previous_registration',
            'individual_id',
            'five_years_in_UK'
        )

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'PREVIOUS_REGISTRATION_DETAILS'


class PreviousRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NannyPreviousRegistrationDetails
        fields = '__all__'


