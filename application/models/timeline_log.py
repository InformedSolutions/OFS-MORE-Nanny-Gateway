from rest_framework import serializers

from timeline_logger.models import TimelineLog


class TimelineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineLog
        fields = '__all__'
