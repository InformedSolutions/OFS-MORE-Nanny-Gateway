"""
Utility functions for generating a new unique application reference number
"""
import json

import requests
from django.conf import settings


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

