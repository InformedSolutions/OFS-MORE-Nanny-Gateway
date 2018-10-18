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
            'lives_with_applicant'
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
        date_of_birth_list = str(data['date_of_birth']).split('-')
        birth_day = date_of_birth_list[2]
        birth_month = date_of_birth_list[1]
        if birth_month == '01':
            birth_month_string = 'Jan'
        elif birth_month == '02':
            birth_month_string = 'Feb'
        elif birth_month == '03':
            birth_month_string = 'Mar'
        elif birth_month == '04':
            birth_month_string = 'Apr'
        elif birth_month == '05':
            birth_month_string = 'May'
        elif birth_month == '06':
            birth_month_string = 'Jun'
        elif birth_month == '07':
            birth_month_string = 'Jul'
        elif birth_month == '08':
            birth_month_string = 'Aug'
        elif birth_month == '09':
            birth_month_string = 'Sep'
        elif birth_month == '10':
            birth_month_string = 'Oct'
        elif birth_month == '11':
            birth_month_string = 'Nov'
        elif birth_month == '12':
            birth_month_string = 'Dec'
        birth_year = date_of_birth_list[0]
        birth_date = birth_day + ' ' + birth_month_string + ' ' + birth_year

        return birth_date

    def get_summary_table(self, i):     #TODO: Fix this so it can return multiple values for any number of children
        child_address = self.get_address()
        row_name = self.get_name()
        return {"name": row_name, "value": child_address, 'pk': self.data['child_id'],
                "reverse": "Childcare-Address-Manual-Entry", 'index': i + 1,
                "change_link_description": "childcare address " + str(i)}
