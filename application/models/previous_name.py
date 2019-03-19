from datetime import date
from uuid import uuid4
from django.db import models
from rest_framework import serializers


class NannyPreviousName(models.Model):
    """
    Model for PREVIOUS_NAME table, used to contain previous
    """

    # Primary key
    previous_name_id = models.UUIDField(primary_key=True, default=uuid4)

    # Foreign key for application id
    application_id = models.UUIDField(blank=True)

    # Actual name fields
    first_name = models.CharField(max_length=200, blank=True)
    middle_names = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)

    # Date fields
    start_day = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_day = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)

    order = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'PREVIOUS_NAME'

    def get_start_date(self):
        return date(self.start_year, self.start_month, self.start_day)

    def set_start_date(self, start_date):
        self.start_year = start_date.year
        self.start_month = start_date.month

    start_date = property(get_start_date, set_start_date)

    def get_end_date(self):
        return date(self.end_year, self.end_month, self.end_day)

    def set_end_date(self, end_date):
        self.end_year = end_date.year
        self.end_month = end_date.month

    end_date = property(get_end_date, set_end_date)


class PreviousNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = NannyPreviousName
        fields = '__all__'

