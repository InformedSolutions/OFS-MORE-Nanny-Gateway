import datetime
from uuid import uuid4

import inflect
from rest_framework import serializers
from django.db import models

from application.models import ApplicantChildrenDetails


class ApplicantAllChildrenDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantChildrenDetails
        fields = '__all__'

    def get_lives_with_applicant(self):
        data = self.data
        if data['lives_with_applicant']:
            name = self.get_name()
            return name

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
        print('Test')
        data = self.data
        child_address = self.get_address()
        birth_date = self.get_birth_date()
        live_with_applicant_name = self.get_lives_with_applicant()

        return [
            {"title": 'Your Children', "id": data['child_id'], "index": 0},

            {"name": "Which of your children live with you?",
             "value": live_with_applicant_name,
             "pk": data['child_id'],
             "index": 1,
             "reverse": "your-children:Your-Children-Details",
             "change_link_description": "which of your children live with you"}
        ]
