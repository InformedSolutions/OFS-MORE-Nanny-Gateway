# ==================================================================================================================== #
# The code that follows is identical to that of django_timeline_log v1.0 models.TimelineLog, with one exception:
# The 'user' field in TimelineLog has been changed from a ForeignKey field to a TextField.
# This is because:
#  - logs are required when an ARC user flags a field.
#  - The ARC users live in the CM database.
#  - We can't ForeignKey across databases, so must use a more rudimentary field type.
#
# Suggested refactor:
#
# 1) Update the TimelineLog model:
#
# TimelineLog.add_to_class('user', models.TextField(null=True))
#
# 2) Create a NannyTimelineLog which is not managed and can act as an interface for the edited TimelineLog:
#
# class NannyTimelineLog(TimelineLog):
#     class Meta:
#         managed = False
#
# Alternatively, consider database routing to ForeignKey into another database:
# https://docs.djangoproject.com/en/1.11/topics/db/multi-db/#topics-db-multi-db-routing
#
# ==================================================================================================================== #

import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.loader import get_template, render_to_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _


logger = logging.getLogger('timeline_logger')


DEFAULT_TEMPLATE = 'timeline_logger/application_action.txt'


@python_2_unicode_compatible
class TimelineLog(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )
    object_id = models.TextField(
        verbose_name=_('object id'),
        blank=True, null=True
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now_add=True)
    extra_data = JSONField(
        verbose_name=_('extra data'),
        null=True, blank=True,
    )

    # XXX: This is a TextField, not a ForeignKey
    user = models.TextField(
        blank=True, null=True,
    )

    template = models.CharField(max_length=200, default=DEFAULT_TEMPLATE)

    class Meta:
        verbose_name = _('timeline log entry')
        verbose_name_plural = _('timeline log entries')

    def __str__(self):
        if self.object_id:
            return "{ct} - {pk}".format(
                ct=self.content_type.name,
                pk=self.object_id
            )

        return ugettext('TimelineLog Object')

    @classmethod
    def log_from_request(cls, request, content_object, template=None, **extra_data):
        """
        Given an ``HTTPRequest`` object and a generic content, it creates a
        ``TimelineLog`` object to store the data of that request.

        :param request: A Django ``HTTPRequest`` object.
        :param content_object: A Django model instance. Any object can be
        related.
        :param template: String representing the template to be used to render
        the message. Defaults to 'default.txt'.
        :param extra_data: A dictionary (translatable into JSON) determining
        specifications of the action performed.
        :return: A newly created ``TimelineLog`` instance.
        """
        try:
            user = request.user
        except AttributeError:
            user = None

        if template is not None:
            # Ensure that the expected template actually exists.
            get_template(template)

        timeline_log = cls.objects.create(
            content_object=content_object,
            extra_data=extra_data or None,
            template=template or DEFAULT_TEMPLATE,
            user=user,
        )
        logger.debug('Logged event in %s %s', content_object._meta.object_name, content_object.pk)
        return timeline_log

    def get_message(self, template=None, **extra_context):
        """
        Gets the 'log' message, describing the event performed.

        :param template: String representing the template to be used to render
        the message. Defaults to ``self.template``.
        :return: The log message string.
        """
        context = {'log': self}
        context.update(**extra_context)
        return render_to_string(template or self.template, context)


# ==================================================================================================================== #
# End of copied code
# ==================================================================================================================== #


from rest_framework import serializers


class TimelineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineLog
        fields = '__all__'
