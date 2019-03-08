from uuid import uuid4

from rest_framework import serializers
from django.db import models
from application.models import NannyApplication

from .applicant_personal_details import ApplicantPersonalDetails

class NannyPreviousRegistrationDetails(models.Model):
    """
    Model for PREVIOUS_REGISTRATION_DETAILS table
    """
    previous_registration_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    personal_detail_id = models.ForeignKey(ApplicantPersonalDetails, on_delete=models.CASCADE,
                                           db_column='personal_detail_id', null=True)
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
    def get_id(cls, previous_registration_id):
        return cls.objects.get(pk=previous_registration_id)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'PREVIOUS_REGISTRATION_DETAILS'

class PreviousRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = NannyPreviousRegistrationDetails
        fields = '__all__'

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return 'Yes'
        else:
            return 'No'

    def get_summary_table(self):
        data = self.data
        previous_registration = data['previous_registration']
        individual_id = data['individual_id']
        five_years_in_UK = data['five_years_in_UK']
        return [
                {"title": "Previous registration", "id": data['previous_registration_id'], "index": 0},
                {"name": "Previously registered with Ofsted?",
                 "value": previous_registration,
                 'pk': data['previous_registration_id'], "index": 1,
                 "reverse": "previous_registration:Previous-Registration",
                 "change_link_description": "whether the applicant has previously registered with Ofsted"},
                {"name": "Individual ID",
                 "value": individual_id,
                 'pk': data['previous_registration_id'], "index": 2,
                 "reverse": "previous_registration:Individual-Id",
                 "change_link_description": "the individual ID"},
                {"name": "Lived in England for more than 5 years?",
                 "value": five_years_in_UK,
                 'pk': data['previous_registration_id'], "index": 3,
                 "reverse": "first-aid:Training-Details",
                 "change_link_description": "whether the applicant has lived in England for more than 5 years"}
            ]
