import json

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ..models import NannyApplication
from ..models import ApplicantPersonalDetails
from ..models import ApplicantHomeAddress


class SummaryTests(TestCase):

    app = None
    personal_details = None

    def setUp(self):
        self.app = NannyApplication.objects.create()
        self.personal_details = ApplicantPersonalDetails.objects.create(
            application_id=self.app
        )

    def test_can_get_home_address_summary(self):
        """
        Test that the summary for a home address is given from the endpoint.
        """
        app_id = self.app.application_id
        pd_id = self.personal_details.personal_detail_id
        prefix = settings.PUBLIC_APPLICATION_URL
        ApplicantHomeAddress.objects.create(
            application_id=self.app,
            personal_detail_id=self.personal_details,
            street_line1="Line1",
            street_line2="Line2",
            town="Town",
            postcode="Postcode")

        get_endpoint = reverse('Summary', kwargs={'name': 'applicant_home_address', 'application_id': app_id})
        response = self.client.get(get_endpoint)

        summary_table = json.loads(response.content)
        self.assertEqual(summary_table[0].get('name'), 'Your home address')
        self.assertEqual(200, response.status_code)
