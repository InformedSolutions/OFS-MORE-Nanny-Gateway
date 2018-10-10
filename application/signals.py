import sys
import traceback

from timeline_logger.models import TimelineLog

from application import models


def timeline_log_pre_save(sender, instance, raw, using, update_fields, **kwargs):
    """
    Receiver function for the timeline logger when post_save() is called on a model which is tracked.
    :param sender:
    :param model_instance:
    :param created:
    :param kwargs:
    :return:
    """
    try:
        current_application_status = models.NannyApplication.objects.get(pk=instance.application_id).application_status
    except AttributeError:
        traceback.print_exc(file=sys.stdout)
        sys.exit('''
            ------------------------------------------------------------------
            Your model doesn't have application_id field, you can't use
            timeline_log without this field in your model.
            ------------------------------------------------------------------
        ''')

    # Check if NannyApplication has been updated. If so, check if applicant has submitted or resubmitted the application
    if isinstance(instance, models.NannyApplication):
        new_application_status = instance.application_status

        if new_application_status == 'SUBMITTED' and current_application_status == 'DRAFTING':
            return __handle_submitted_application(instance)

        elif new_application_status == 'SUBMITTED' and current_application_status == 'FURTHER_INFORMATION':
            return __handle_resubmitted_application(instance)

    else:
        # Grab instance's existing data from the database.
        old_instance = instance._meta.default_manager.get(pk=instance.pk)

        if current_application_status == 'FURTHER_INFORMATION':
            # update_fields does not appear to be set in the Serializer save() method so will loop through all attrs instead.
            update_fields = [field for field in instance.timelog_fields if getattr(instance, field) != getattr(old_instance, field)]

            for field in update_fields:
                __handle_updated_field(field)


def __handle_submitted_application(instance):
    pass

def __handle_resubmitted_application(instance):
    pass

def __handle_updated_field(field):
    pass
