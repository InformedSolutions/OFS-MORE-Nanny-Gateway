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
    convictions = models.NullBooleanField(blank=True, null=True, default=None)
    lived_abroad = models.NullBooleanField(default=None)
    is_ofsted_dbs = models.NullBooleanField(blank=True, null=True, default=None)
    on_dbs_update_service = models.NullBooleanField(blank=True, null=True, default=None)
    within_three_months = models.NullBooleanField(blank=True, null=True, default=None)
    certificate_information = models.TextField(blank=True)

    @property
    def timelog_fields(self):
        """
        Specify which fields to track in this model once application is returned.
        :return: tuple of fields which needs update tracking when application is returned
        """
        return (
            'lived_abroad',
            'dbs_number',
            'convictions',
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

        return_json = [
            {"title": "Criminal record checks", "id": fields['dbs_id']},
            {"name": "Have you lived outside of the UK in the last 5 years?",
             "value": self.get_bool_as_string(fields['lived_abroad']),
             "reverse": "dbs:Lived-Abroad-View",
             "change_link_description": "answer on lived abroad"},
            {"name": "Do you have an Ofsted DBS Check?",
             "value": self.get_bool_as_string(fields['is_ofsted_dbs']),
             "reverse": "dbs:DBS-Type-View",
             "change_link_description": "answer to having an Ofsted DBS Check"},
        ]

        if fields['is_ofsted_dbs']:
            dbs_page_link = 'dbs:Capita-DBS-Details-View'
        elif not fields['is_ofsted_dbs']:
            dbs_page_link = 'dbs:Non-Capita-DBS-Details-View'

        dbs_number_data = {
            "name": "DBS certificate number",
            "value": fields['dbs_number'],
            "reverse": dbs_page_link,
            "change_link_description": "DBS certificate number",
        }

        convictions_data = {
            "name": "Do you have any criminal cautions or convictions?",
            "value": self.get_bool_as_string(fields['convictions']),
            "reverse": "dbs:Capita-DBS-Details-View",
            "change_link_description": "answer on criminal cautions or convictions"
        }

        on_dbs_update_service_data = {
            "name": "Are you on the DBS update service?",
            "value": self.get_bool_as_string(fields['on_dbs_update_service']),
            "reverse": "dbs:DBS-Update-Service-Page",
            "change_link_description": "answer to being on the DBS update service"
        }

        if fields['is_ofsted_dbs']:
            return_json.append(dbs_number_data)
            return_json.append(convictions_data)
        elif not fields['is_ofsted_dbs']:
            return_json.append(on_dbs_update_service_data)
            return_json.append(dbs_number_data)

        return return_json
