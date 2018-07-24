from uuid import uuid4

from rest_framework import serializers
from django.db import models
from .nanny_application import NannyApplication
from .applicant_personal_details import ApplicantPersonalDetails


class ApplicantHomeAddress(models.Model):
    """
        Model for Nanny Application table
    """
    # Managers
    objects = models.Manager()

    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    personal_detail_id = models.ForeignKey(ApplicantPersonalDetails, on_delete=models.CASCADE,
                                           db_column='personal_detail_id')
    home_address_id = models.UUIDField(primary_key=True, default=uuid4)
    street_line1 = models.CharField(max_length=100, blank=True, null=True)
    street_line2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    current_address = models.NullBooleanField(blank=True, null=True, default=None)
    childcare_address = models.NullBooleanField(blank=True, null=True, default=None)
    move_in_month = models.IntegerField(blank=True, null=True)
    move_in_year = models.IntegerField(blank=True, null=True)

    @classmethod
    def get_id(cls, home_address_id):
        return cls.objects.get(pk=home_address_id)

    class Meta:
        db_table = 'APPLICANT_HOME_ADDRESS'


class ApplicantHomeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantHomeAddress
        fields = '__all__'

    def get_address(self):
        data = self.data
        return str(data['street_line1']) + ', ' + str(data['street_line2']) + ', ' \
               + str(data['town']) + ', ' + str(data['postcode'])

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return "Yes"
        else:
            return "No"

    def get_summary_table(self):
        data = self.data
        home_address = self.get_address()
        return [
                {"name": "Your home address", "value": home_address, 'pk': data['home_address_id'], "index": 3,
                 "reverse": "personal-details:Personal-Details-Manual-Address"},
                {"name": "Is this where you will look after the children?",
                 "value": self.get_bool_as_string(data['childcare_address']),
                 'pk': data['home_address_id'], "index": 4,
                 "reverse": "Childcare-Address-Location"}
            ]

