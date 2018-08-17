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
    application_id = models.ForeignKey(
        NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    dbs_number = models.CharField(max_length=100)
    convictions = models.NullBooleanField(blank=True, null=True, default=None)

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
             "reverse": "dbs:Details"},
            {"name": "Do you have any cautions or convictions?",
             "value": self.get_bool_as_string(fields['convictions']),
             "reverse": "dbs:Details"}
        ]