"""
Utility functions for generating a new unique application reference number
"""
import requests
from django.conf import settings
from ..models import ApplicantPersonalDetails, Payment, NannyApplication
from ..messaging import SQSHandler


sqs_handler = SQSHandler(settings.PAYMENT_NOTIFICATIONS_QUEUE_NAME)


def create_application_reference():
    """
    Function for getting the next available URN from NOO such that it can be allocated to a Childminder application
    :return: a unique reference number for an application
    """
    integration_adapter_endpoint = settings.INTEGRATION_ADAPTER_URL
    response = requests.get(integration_adapter_endpoint + '/api/v1/urns/')

    response_body_as_json = response.json()
    if response_body_as_json.get('error'):
        raise Exception(response_body_as_json['error'])
    else:
        urn = response_body_as_json['URN']

    return str(urn)


def send_payment_notification(application_id, amount):
    """
    Method for sending an ad-hoc payment to NOO
    :param application_id: the application identifier
    :param application_reference: the application reference number (URN)
    :param payment_reference: the payment reference number
    :param amount: the amount charged
    """
    if isinstance(amount, str):
        amount = int(amount)

    app_cost_float = float(amount / 100)
    msg_body = __build_message_body(application_id, format(app_cost_float, '.4f'))
    sqs_handler.send_message(msg_body)


def __build_message_body(application_id, amount):
    """
    Helper method to build an SQS request to be picked up by the Integration Adapter component
    for relay to NOO
    :return: an SQS request that can be consumed up by the Integration Adapter component
    """
    applicant_name = ApplicantPersonalDetails.objects.get(application_id=application_id)
    payment_reference = Payment.objects.get(application_id=application_id).payment_reference
    application_reference = NannyApplication.objects.get(pk=application_id).application_reference

    if len(applicant_name.middle_names):
        applicant_name = applicant_name.last_name + ',' + applicant_name.first_name + " " + applicant_name.middle_names
    else:
        applicant_name = applicant_name.last_name + ',' + applicant_name.first_name

    return {
        "payment_action": "SC1",
        "payment_ref": payment_reference,
        "payment_amount": amount,
        "urn": str(settings.PAYMENT_URN_PREFIX) + application_reference,
        "setting_name": applicant_name
    }
