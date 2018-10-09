from uuid import uuid4

from rest_framework import serializers
from django.db import models
from .nanny_application import NannyApplication


class ApplicantPersonalDetails(models.Model):
    """
        Model for Nanny Application table
    """
    # Managers
    objects = models.Manager()

    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    personal_detail_id = models.UUIDField(primary_key=True, default=uuid4)
    date_of_birth = models.DateField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True, max_length=100)
    middle_names = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    lived_abroad = models.NullBooleanField(blank=True, null=True)
    post_certificate_declaration = models.NullBooleanField(blank=True, null=True)

    @classmethod
    def get_id(cls, personal_detail_id):
        return cls.objects.get(pk=personal_detail_id)

    @property
    def get_full_name(self):
        return "{0}{1} {2}".format(self.first_name, (" "+self.middle_names if self.middle_names else ""), self.last_name)

    class Meta:
        db_table = 'APPLICANT_PERSONAL_DETAILS'


class ApplicantPersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantPersonalDetails
        fields = '__all__'

    def get_name(self):
        data = self.data
        if data['middle_names']:
            return str(data['first_name']) + " " + str(data['middle_names']) + " " + str(data['last_name'])
        else:
            return str(data['first_name']) + " " + str(data['last_name'])

    def get_summary_table(self):
        data = self.data
        return [
                {"title": "Your personal details", "id": data['personal_detail_id'], "index": 0},
                {"name": "Full name",
                 "value": self.get_name(),
                 'pk': data['personal_detail_id'], "index": 1,
                 "reverse": "personal-details:Personal-Details-Name"},
                {"name": "Date of birth",
                 "value": str(data['date_of_birth']), 'pk': data['personal_detail_id'], "index": 2,
                 "reverse": "personal-details:Personal-Details-Date-Of-Birth"},
                {"name": "Have you lived outside of the UK in the last 5 years?",
                 "value": 'Yes' if data['lived_abroad'] else 'No', 'pk': data['personal_detail_id'], "index": 4,
                 "reverse": "personal-details:Personal-Details-Lived-Abroad"}
            ]
