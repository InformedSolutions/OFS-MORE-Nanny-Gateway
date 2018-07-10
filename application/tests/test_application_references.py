"""
Tests for assuring the application reference number generation process
"""
import re
from uuid import UUID

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ..models import ApplicationReference, NannyApplication, json
from ..application_reference_generator import create_application_reference, allocate_reference_number
from ..views import retrieve_reference_number


class ApplicationReferenceTests(TestCase):

    test_application_id = 'f8c42666-1367-4878-92e2-1cee6ebcb48c'
    test_discriminator = settings.APPLICATION_PREFIX

    def test_application_discriminator_applied(self):
        test_reference_number = create_application_reference()
        reference_number_discriminator = test_reference_number[:2]
        self.assertEqual(reference_number_discriminator, self.test_discriminator)

    def test_application_reference_seeding_number_set(self):
        # Test to assert seed reference is set at 1000000
        test_reference_number = create_application_reference()
        reference_number_without_prefix = test_reference_number[2:]
        self.assertEqual(reference_number_without_prefix, '1000001')

    def test_can_create_application_reference_number_with_delimiter_prefixed(self):
        test_reference_number = create_application_reference()
        self.assertIsNotNone(test_reference_number)
        self.assertTrue(re.match(r'(' + settings.APPLICATION_PREFIX + ')([0-9]{7})', test_reference_number))

    def test_application_reference_number_rolls(self):
        create_application_reference()
        current_reference = ApplicationReference.objects.all().first()
        self.assertEqual(current_reference.reference, 1000001)

        create_application_reference()
        current_reference = ApplicationReference.objects.all().first()
        self.assertEqual(current_reference.reference, 1000002)

    def test_can_assign_application_from_view_tier(self):
        test_application = NannyApplication.objects.create(
            application_id=(UUID(self.test_application_id)),
        )

        allocate_reference_number(test_application.application_id)

        test_application.refresh_from_db()

        self.assertIsNotNone(test_application.application_reference)
        self.assertEqual(test_application.application_reference, str(self.test_discriminator + '1000001'))

    def test_application_reference_retained_once_assigned(self):
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
        self.assertEqual(test_application.application_reference, str(self.test_discriminator + '1000001'))

    def test_can_reconcile_api_endpoint_for_reference_allocation(self):
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

