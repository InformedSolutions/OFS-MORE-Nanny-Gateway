from uuid import uuid4
import datetime

from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class ApplicantPersonalDetails(models.Model):
    """
    Model for APPLICANT_PERSONAL_DETAILS table
    """
    # Managers
    objects = models.Manager()

    application_id = models.OneToOneField(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    personal_detail_id = models.UUIDField(primary_key=True, default=uuid4)
    date_of_birth = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(blank=True, null=True, max_length=100)
    middle_names = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    # Date fields for current name
    name_start_day = models.IntegerField(blank=True, null=True)
    name_start_month = models.IntegerField(blank=True, null=True)
    name_start_year = models.IntegerField(blank=True, null=True)
    name_end_day = models.IntegerField(blank=True, null=True)
    name_end_month = models.IntegerField(blank=True, null=True)
    name_end_year = models.IntegerField(blank=True, null=True)
    # Date fields for current address
    moved_in_date = models.DateField(blank=True, null=True)
    moved_out_date = models.DateField(blank=True, null=True)

    known_to_social_services = models.NullBooleanField(blank=True, null=True, default=None)
    reasons_known_to_social_services = models.TextField(null=True, default="")


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
            'known_to_social_services',
            'reasons_known_to_social_services'
        )

    @classmethod
    def get_id(cls, personal_detail_id):
        return cls.objects.get(pk=personal_detail_id)

    @property
    def get_full_name(self):
        return "{0}{1} {2}".format(self.first_name, (" " + self.middle_names if self.middle_names else ""),
                                   self.last_name)

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
        birth_date_datetime = datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        birth_date = birth_date_datetime.strftime('%d/%m/%Y')

        moved_in_date_datetime = datetime.datetime.strptime(data['moved_in_date'], '%Y-%m-%d').date()
        moved_in_date = moved_in_date_datetime.strftime('%d/%m/%Y')

        summary_table_list = [
            {"title": "Your personal details", "id": data['personal_detail_id'], "index": 0},
            {"name": "Title",
             "value": data['title'],
             'pk': data['personal_detail_id'], "index": 1,
             "reverse": "personal-details:Personal-Details-Name",
             "change_link_description": "title"},
            {"name": "Your name",
             "value": self.get_name(),
             'pk': data['personal_detail_id'], "index": 2,
             "reverse": "personal-details:Personal-Details-Name",
             "change_link_description": "your name"},
            {"name": "Date of birth",
             "value": birth_date, 'pk': data['personal_detail_id'], "index": 3,
             "reverse": "personal-details:Personal-Details-Date-Of-Birth",
             "change_link_description": "your date of birth"},
            {"name": "Moved in date",
                    "value": moved_in_date, "index": 4,
                "reverse": "personal-details:Personal-Details-Manual-Address"},
            {"name": "Known to council social Services?",
             "value": 'Yes' if data['known_to_social_services'] else 'No', 'pk': data['personal_detail_id'], "index": 5,
             "reverse": "personal-details:Personal-Details-Your-Children"},
        ]

        if data['known_to_social_services'] is True:
            summary_table_list.append(
                {"name": "Tell us why",
                 "value": data['reasons_known_to_social_services'], 'pk': data['personal_detail_id'], "index": 5,
                 "reverse": 'personal-details:Personal-Details-Your-Children'},
            )

        return summary_table_list
