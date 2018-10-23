from uuid import uuid4
from django.db import models
from rest_framework import serializers

from .nanny_application import NannyApplication


class DbsCheck(models.Model):
    """
    Model for DBS_CHECK table
    """
    objects = models.Manager()

    dbs_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    dbs_number = models.CharField(max_length=100, null=True)
    has_convictions = models.NullBooleanField(blank=True, null=True, default=None)
    lived_abroad = models.BooleanField(default=None)
    is_ofsted_dbs = models.NullBooleanField(blank=True, null=True, default=None)
    on_dbs_update_service = models.NullBooleanField(blank=True, null=True, default=None)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        :return: tuple of fields which needs update tracking when application is returned
        """
        return (
            'lived_abroad',
            'dbs_number',
            'has_convictions',
            'on_dbs_update_service'
        )

    class Meta:
        db_table = 'DBS_CHECK'


class DbsCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbsCheck
        fields = '__all__'

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return 'Yes'
        else:
            return 'No'

    def get_summary_table(self):
        fields = self.data
        return [
            {"title": "Criminal record (DBS) check", "id": fields['dbs_id']},
            {"name": "DBS certificate number", "value": fields['dbs_number'],
             "reverse": "dbs:Details",
             "change_link_description": "DBS certificate number"},
            {"name": "Do you have any criminal cautions or convictions?",
             "value": self.get_bool_as_string(fields['convictions']),
             "reverse": "dbs:Details",
             "change_link_description": "answer on criminal cautions or convictions"}
        ]
