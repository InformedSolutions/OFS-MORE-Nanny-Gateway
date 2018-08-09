"""
Tests for assuring the application reference number generation process
"""
import re
from unittest import mock
from uuid import UUID

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ..models import NannyApplication
from ..application_reference_generator import allocate_reference_number


class ApplicationReferenceTests(TestCase):
    test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
    test_discriminator = settings.APPLICATION_PREFIX

    def setUp(self):
        pass

    def test_can_assign_application_from_view_tier(self):
        with mock.patch('application.services.noo_integration_service.create_application_reference') \
                as application_reference_mock:
            mock_urn = 'TESTURN'
            application_reference_mock.return_value = mock_urn
            test_application = NannyApplication.objects.create(
                application_id=(UUID(self.test_application_id)),
            )

            allocate_reference_number(test_application.application_id)

            test_application.refresh_from_db()

            self.assertIsNotNone(test_application.application_reference)
            self.assertEqual(test_application.application_reference, mock_urn)

    def test_application_reference_retained_once_assigned(self):
        with mock.patch('application.services.noo_integration_service.create_application_reference') \
                as application_reference_mock:
            mock_urn = 'TESTURN'
            application_reference_mock.return_value = mock_urn
            test_application = NannyApplication.objects.create(
                application_id=(UUID(self.test_application_id)),
            )

            allocate_reference_number(test_application.application_id)

            test_application.refresh_from_db()

            # Invoke allocation method for a second time
            allocate_reference_number(test_application.application_id)
            test_application.refresh_from_db()

            # Check reference number matches initial invocation only
            self.assertIsNotNone(test_application.application_reference)
            self.assertEqual(test_application.application_reference, mock_urn)

    def test_can_reconcile_api_endpoint_for_reference_allocation(self):
        with mock.patch('application.services.noo_integration_service.create_application_reference') \
                as application_reference_mock:
            mock_urn = 'TESTURN'
            application_reference_mock.return_value = mock_urn
            test_application = NannyApplication.objects.create(
                application_id=(UUID(self.test_application_id)),
            )

            get_endpoint = reverse('Assign-Application-Reference-View', kwargs={'application_id': self.test_application_id})
            response = self.client.get(get_endpoint)

            test_application.refresh_from_db()

            self.assertIsNotNone(test_application.application_reference)
            self.assertIsNotNone(response)

            response_body = response.json()
            self.assertIsNotNone(response_body['reference'])
