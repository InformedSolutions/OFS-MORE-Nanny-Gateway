from django.conf import settings
from django.test import TestCase
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

        url = prefix + '/api/v1/summary/applicant_home_address/' + str(app_id)
        response = self.client.get(url)

        self.assertEqual(301, response.status_code)
