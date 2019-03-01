from uuid import uuid4

from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class ApplicantPersonalDetails(models.Model):
    """
    Model for APPLICANT_PERSONAL_DETAILS table
    """
    # Managers
    objects = models.Manager()

    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    personal_detail_id = models.UUIDField(primary_key=True, default=uuid4)
    date_of_birth = models.DateField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True, max_length=100)
    middle_names = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
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

        summary_table_list = [
            {"title": "Your personal details", "id": data['personal_detail_id'], "index": 0},
            {"name": "Your name",
             "value": self.get_name(),
             'pk': data['personal_detail_id'], "index": 1,
             "reverse": "personal-details:Personal-Details-Name",
             "change_link_description": "your name"},
            {"name": "Date of birth",
             "value": birth_date, 'pk': data['personal_detail_id'], "index": 2,
             "reverse": "personal-details:Personal-Details-Date-Of-Birth",
             "change_link_description": "your date of birth"},
            {"name": "Known to council social Services?",
             "value": 'Yes' if data['known_to_social_services'] else 'No', 'pk': data['personal_detail_id'], "index": 4,
             "reverse": "personal-details:Personal-Details-Your-Children"},
        ]

        if data['known_to_social_services'] is True:
            summary_table_list.append(
                {"name": "Tell us why",
                 "value": data['reasons_known_to_social_services'], 'pk': data['personal_detail_id'], "index": 5,
                 "reverse": 'personal-details:Personal-Details-Your-Children'},
            )

        return summary_table_list
