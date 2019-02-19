"""
Utility functions for generating a new unique application reference number
"""

from .models import NannyApplication
from application.services import noo_integration_service
import logging

logger = logging.getLogger(__name__)


def allocate_reference_number(application_id):
    """
    Method for allocating a reference number to an application
    """
    application = NannyApplication.objects.get(pk=application_id)

    # If an application reference number has not yet been allocated
    # assign an persist value
    if application.application_reference is None:
        application.application_reference = noo_integration_service.create_application_reference()
        application.save()
