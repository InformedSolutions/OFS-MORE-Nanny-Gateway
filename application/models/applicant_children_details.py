import datetime
from uuid import uuid4

import inflect
from rest_framework import serializers
from django.db import models
from .nanny_application import NannyApplication


class ApplicantChildrenDetails(models.Model):
    """
    Model for APPLICANT_CHILDREN_DETAILS table
    """
    # Managers
    objects = models.Manager()

    child_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    child = models.IntegerField(null=True, blank=True)
    lives_with_applicant = models.NullBooleanField(null=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_names = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    birth_day = models.IntegerField(blank=True)
    birth_month = models.IntegerField(blank=True)
    birth_year = models.IntegerField(blank=True)
    date_created = models.DateTimeField(blank=True, null=True)
    street_line1 = models.CharField(max_length=100, blank=True, null=True)
    street_line2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=True, null=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        :return: tuple of fields which needs update tracking when application is returned
        """
        return (
            'date_of_birth',
            'first_name',
            'middle_names',
            'last_name',
            'lived_abroad',
            'your_children',
            'lives_with_applicant',
            'child',
        )

    @classmethod
    def get_id(cls, child_id):
        return cls.objects.get(pk=child_id)

    class Meta:
        db_table = 'APPLICANT_CHILDREN_DETAILS'


class ApplicantChildrenDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantChildrenDetails
        fields = '__all__'

    def get_name(self):
        data = self.data
        if data['middle_names']:
            return str(data['first_name']) + " " + str(data['middle_names']) + " " + str(data['last_name'])
        else:
            return str(data['first_name']) + " " + str(data['last_name'])

    def get_title_row(self):
        return {"title": "Childcare address", "id": self.data['childcare_address_id'], "index": 0}

    def get_address_ord(self, i):
        """
        get ordinal value of this childcare address
        :param i: index of address
        :return:
        """
        formatter = inflect.engine()
        return formatter.number_to_words(formatter.ordinal(i)).title()

    def get_address(self):
        data = self.data
        return str(data['street_line1']) + ', ' + str(data['street_line2']) + ', ' \
               + str(data['town']) + ', ' + str(data['postcode'])

    def get_birth_date(self):
        data = self.data
        birth_day = data['birth_day']
        birth_month = data['birth_month']
        birth_year = data['birth_year']

        birth_datetime = datetime.datetime(birth_year, birth_month, birth_day)
        return birth_datetime.strftime('%d %b %Y')

    def get_summary_table(self):
        data = self.data
        child_address = self.get_address()
        birth_date = self.get_birth_date()
        live_with_applicant_name = self.get_lives_with_applicant()

        return [
            {"title": self.get_name(), "id": data['child_id'], "index": 0},

            {"name": "Name",
             "value": self.get_name(),
             'pk': data['child_id'], "index": 1,
             "reverse": "your-children:Your-Children-Details",
             "change_link_description": "child's name"},

            {"name": "Date of birth",
             "value": birth_date, 'pk': data['child_id'], "index": 2,
             "reverse": "your-children:Your-Children-Details",
             "change_link_description": "child's date of birth"},

            {"name": "Address",
             "value": child_address, 'pk': data['child_id'], "index": 3,
             "reverse": "your-children:Your-Children-Manual-address",
             "change_link_description": "child's address"},
        ]
