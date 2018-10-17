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
    your_children = models.NullBooleanField(blank=True, null=True)


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
        return [
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
                {"name": "Have you lived abroad in the last 5 years?",
                 "value": 'Yes' if data['lived_abroad'] else 'No', 'pk': data['personal_detail_id'], "index": 4,
                 "change_link_description": "answer on living abroad in the last 5 years",
                 "reverse": "personal-details:Personal-Details-Lived-Abroad"},
                {"name": "Do you have any children of your own under 16?",
                 "value": 'Yes' if data['your_children'] else 'No', 'pk': data['personal_detail_id'], "index": 5,
                 "change_link_description": "children of your own",
                 "reverse": "personal-details:Personal-Details-Your-Children"},

            ]
      