from uuid import uuid4
from django.db import models
from rest_framework import serializers


class ArcComments(models.Model):
    """
    Model for ARC_COMMENTS table.
    """
    objects = models.Manager()

    review_id = models.UUIDField(primary_key=True, default=uuid4, unique=True),
    table_pk = models.UUIDField(blank=True)
    field_name = models.CharField(max_length=40, blank=True)
    comment = models.CharField(max_length=100, blank=True)
    flagged = models.BooleanField()

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(application_id=app_id)

    class Meta:
        db_table = 'ARC_COMMENTS'


class ArcCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArcComments
        fields = '__all__'
