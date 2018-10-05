from uuid import uuid4

from rest_framework import serializers
from django.db import models

from .nanny_application import NannyApplication


class ChildcareTraining(models.Model):
    """
    Model for Childcare Training table.
    """
    objects = models.Manager()

    childcare_training_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    level_2_training = models.NullBooleanField(blank=True, null=True, default=None)
    common_core_training = models.NullBooleanField(blank=True, null=True, default=None)
    no_training = models.NullBooleanField(blank=True, null=True, default=None)

    @classmethod
    def get_id(cls, app_id):
        return cls.objects.get(pk=app_id)

    class Meta:
        db_table = 'CHILDCARE_TRAINING'
        # app_label = 'nanny_models'


class ChildcareTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildcareTraining
        fields = '__all__'

    def get_bool_as_string(self, bool_field):
        if bool_field:
            return 'Yes'
        else:
            return 'No'

    def get_summary_table(self):
        data = self.data
        level_2_training = data['level_2_training']
        common_core_training = data['common_core_training']
        no_training = data['no_training']
        if not no_training:
            if level_2_training and common_core_training:
                childcare_training = 'Childcare qualification (level 2 or higher), Training in common core skills'
            elif level_2_training and not common_core_training:
                childcare_training = 'Childcare qualification (level 2 or higher)'
            elif not level_2_training and common_core_training:
                childcare_training = 'Training in common core skills'
        else:
            childcare_training = 'None'
        return [
                {"title": "Childcare training", "id": data['childcare_training_id']},
                {"name": "What type of childcare course have you completed?",
                 "value": childcare_training,
                 'pk': data['childcare_training_id'],
                 "reverse": "Type-Of-Childcare-Training"}
            ]
