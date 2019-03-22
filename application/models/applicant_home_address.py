from uuid import uuid4

from rest_framework import serializers
from django.db import models
from .nanny_application import NannyApplication
from .applicant_personal_details import ApplicantPersonalDetails


class ApplicantHomeAddress(models.Model):
    """
    Model for APPLICANT_HOME_ADDRESS table.
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

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        :return: tuple of fields which needs update tracking when application is returned
        """
        return (
            'street_line1',
            'street_line2',
            'town',
            'county',
            'country',
            'postcode',
            'current_address',
            'move_in_month',
            'move_in_year'
        )

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
        return ', '.join([self.data[p]
                          for p in ('street_line1', 'street_line2', 'town', 'county', 'postcode', 'country')
                          if self.data[p]])

    def get_bool_as_string(self, bool_field):
        return 'Yes' if bool_field else 'No'

    def get_summary_table(self):
        return [
            {"name": "Your home address",
             "value": self.get_address(),
             'pk': self.data['home_address_id'],
             "index": 3,
             "section": "applicant_personal_details_section",
             "reverse": "personal-details:Personal-Details-Manual-Address",
             "change_link_description": "your home address"},
            {"name": "Do you currently live and work at the same address?",
             "value": self.get_bool_as_string(self.data['childcare_address']),
             "section": "childcare_address_section",
             'pk': self.data['home_address_id'],
             "index": 1,
             "reverse": "Childcare-Address-Location",
             "change_link_description": "answer on working and living at the same address"}
        ]

