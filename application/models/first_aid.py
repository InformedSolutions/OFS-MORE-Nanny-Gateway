from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class FirstAidTraining(models.Model):
    """
    Model for FIRST_AID_TRAINING table
    """
    objects = models.Manager()

    first_aid_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    training_organisation = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)
    course_date = models.DateField()
    show_certificate = models.NullBooleanField(blank=True, null=True, default=None)
    renew_certificate = models.NullBooleanField(blank=True, null=True, default=None)

    class Meta:
        db_table = 'FIRST_AID_TRAINING'


class FirstAidTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstAidTraining
        fields = '__all__'

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return 'Yes'
        else:
            return 'No'

    def get_summary_table(self):
        data = self.data
        course_date_list = str(data['course_date']).split('-')
        course_day = course_date_list[2]
        course_month = course_date_list[1]
        course_year = course_date_list[0]
        course_date = course_day + '/' + course_month + '/' + course_year
        return [
                {"title": "First aid training", "id": data['first_aid_id'], "index": 0},
                {"name": "Training organisation",
                 "value": data['training_organisation'],
                 'pk': data['first_aid_id'], "index": 1,
                 "reverse": "first-aid:Training-Details",
                 "change_link_description": "training organisation"},
                {"name": "Title of training course",
                 "value": data['course_title'],
                 'pk': data['first_aid_id'], "index": 2,
                 "reverse": "first-aid:Training-Details",
                 "change_link_description": "course title"},
                {"name": "Date you completed course",
                 "value": course_date,
                 'pk': data['first_aid_id'], "index": 3,
                 "reverse": "first-aid:Training-Details",
                 "change_link_description": "course completion date"}
            ]
