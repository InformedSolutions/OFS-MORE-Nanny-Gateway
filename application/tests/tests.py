from django.conf import settings
from django.test import TestCase


class NannyGatewayTests(TestCase):

    def test_get_request_returns_404_for_childminder_app_types(self):
        """
        Test that making a query for an application id that is not associated with a record returns a 404 response code.
        """
        prefix = settings.PUBLIC_APPLICATION_URL
        response = self.client.get(prefix + '/api/v1/user/?application_type=CHILDMINDER')

        self.assertEqual(response.status_code, 404)
