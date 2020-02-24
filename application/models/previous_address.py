from uuid import uuid4
from datetime import date

from rest_framework import serializers
from django.db import models


class PreviousAddress(models.Model):

    # Options for type discriminator
    previous_address_types = (
        ('APPLICANT', 'APPLICANT'),
    )

    # Primary key
    previous_address_id = models.UUIDField(primary_key=True, default=uuid4)

    # Person the address is for. Application id is used to represent applicant
    person_id = models.UUIDField(blank=True)

    # Type discriminator
    person_type = models.CharField(choices=previous_address_types, max_length=50, blank=True)

    street_line1 = models.CharField(max_length=100, blank=True)
    street_line2 = models.CharField(max_length=100, blank=True)
    town = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=100, blank=True)

    # Date fields
    moved_in_date = models.DateField(blank=True, null=True)
    moved_out_date = models.DateField(blank=True, null=True)

    order = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'PREVIOUS_ADDRESS'

    # noinspection SpellCheckingInspection
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
            'moved_in_date',
            'moved_out_date',
        )


class PreviousAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousAddress
        fields = '__all__'

    def get_address(self):
        return ', '.join([self.data[p]
                          for p in ('street_line1', 'street_line2', 'town', 'county', 'country', 'postcode', 'country')
                          if self.data[p]])

    def get_summary_table(self):
        return [
            {"name": "Previous home address",
             "value": self.get_address(),
             'pk': self.data['home_address_id'],
             "index": 3,
             "section": "applicant_personal_details_section",
             "reverse": "personal-details:Personal-Details-Manual-Address",
             "change_link_description": "previous home address"},
        ]
