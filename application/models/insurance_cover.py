from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class InsuranceCover(models.Model):
    """
    Model for INSURANCE_COVER table
    """
    objects = models.Manager()

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

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return 'Yes'
        else:
            return 'No'

    def get_summary_table(self):
        data = self.data
        return [
                {"title": "Insurance cover", "id": data['insurance_cover_id']},
                {"name": "Do you have public liability insurance?",
                 "value": self.get_bool_as_string(data['public_liability']),
                 'pk': data['insurance_cover_id'],
                    "reverse": "insurance:Public-Liability"}
            ]


