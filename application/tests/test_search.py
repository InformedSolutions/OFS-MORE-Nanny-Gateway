"""
Tests for assuring that ArcSearch functionality is working.
"""
import uuid

import rest_framework
from django.test import TestCase, tag

from ..models import NannyApplication, ApplicantHomeAddress, ApplicantPersonalDetails, ChildcareAddress
from ..views import ArcSearchListView


class MockSearchRequest:
    """
    Mock Search Request for calling ArcSearchListView.list() with.
    This class exists almost solely to implement the __getattr__ method.
    """

    def __init__(self, name="", date_of_birth="", home_postcode="", care_location_postcode="",
                 application_reference=""):
        self.query_params = {'name': name,
                             'date_of_birth': date_of_birth,
                             'home_postcode': home_postcode,
                             'care_location_postcode': care_location_postcode,
                             'application_reference': application_reference}

    def __getattr__(self, attr):
        return self.get(attr)


class SearchTests(TestCase):

    # Utility Functions

    def create_applications(self):
        """
        Creates multiple applications for use in test database.
        :return:
        """
        self.create_application(application_id='1e4f8ae7-bf96-497e-bf02-ebe97afb58c5',
                                first_name='Peter',
                                last_name='Jameson',
                                date_of_birth='2002-04-03',
                                home_address_postcode='M45 7PS',
                                childcare_postcode_list=['LL19 9LT'],
                                application_reference="NA0000001")
        self.create_application(application_id='26b0a49b-160f-4a8b-b3df-e888092c77e9',
                                first_name='Wock',
                                last_name='Peter',
                                date_of_birth='1997-06-21',
                                home_address_postcode='CM21 9EP',
                                childcare_postcode_list=['PO16 9AJ', 'DA1 4AL'])
        self.create_application(application_id='24e6a689-5434-40a0-80d2-bab6e121fcaa',
                                first_name='Donald',
                                last_name='Goofington',
                                date_of_birth='1990-03-06',
                                home_address_postcode='PH50 4RE',
                                childcare_postcode_list=['NE35 9NQ', 'SW1X 0EP', 'B42 2NJ'])

    def create_application(self, application_id: str, first_name: str, last_name: str, date_of_birth: str,
                           home_address_postcode: str,
                           childcare_postcode_list: list, application_reference: str = None) -> None:
        """
        Creates a Test application (with minimum required information for testing) with the given parameters.
        :param application_id: application_id -- NannyApplication
        :param first_name: applicant's first name -- ApplicantPersonalDetails
        :param last_name: applicant's last name -- ApplicantPersonalDetails
        :param date_of_birth: applicant's date of birth -- ApplicantPersonalDetails
        :param home_address_postcode: applicant's home address postcode -- ApplicantHomeAddress # One-to-One
        :param childcare_postcode_list: applicant's childcare postcode(s) in list format -- ChildcareAddress # Many-To-One
        :param application_reference: application's reference number, null by default -- NannyApplication
        :return: Void

        Note: A random UUID4 is used to create each database entry.
            This could potentially lead to slight differences when re-running tests.
        """

        application = NannyApplication.objects.create(application_id=application_id,
                                                      application_reference=application_reference)

        personal_details = ApplicantPersonalDetails.objects.create(
            personal_detail_id=uuid.uuid4(),
            application_id=application,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth)

        ApplicantHomeAddress.objects.create(home_address_id=uuid.uuid4(),
                                            personal_detail_id=personal_details,
                                            application_id=application,
                                            postcode=home_address_postcode)

        for childcare_postcode in childcare_postcode_list:
            ChildcareAddress.objects.create(childcare_address_id=uuid.uuid4(),
                                            application_id=application,
                                            postcode=childcare_postcode)

    # Unit Tests
    ## General Tests

    @tag('unit')
    def test_search_returns_rest_framework_response(self):
        """
        Test to see if the search returns a Response object.
        """
        mock_request = MockSearchRequest()
        response = ArcSearchListView().list(mock_request)
        self.assertEqual(type(response), rest_framework.response.Response)

    @tag('unit')
    def test_response_contains_data_list(self):
        """
        Test to see if the response has a data parameter and that the value is of type list.
        """
        mock_request = MockSearchRequest()
        response = ArcSearchListView().list(mock_request)
        self.assertEqual(type(response.data), list)

    # Integration Tests
    ## General Tests

    @tag('integration')
    def test_search_return_no_results(self):
        """
        Test to see if the a search can return no results.
        """
        self.create_applications()
        mock_request = MockSearchRequest(name='NotInDB')

        response = ArcSearchListView().list(mock_request)

        self.assertEqual(type(response.data), list)
        self.assertTrue(len(response.data) == 0)

    @tag('integration')
    def test_search_return_all_results(self):
        """
        Test to see if the search returns all results when given empty string parameters.
        """
        self.create_applications()
        mock_request = MockSearchRequest()

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 3)

        ## Name Tests

    @tag('integration')
    def test_search_single_app_name(self):
        """
        Test to search for a name with one result.
        """
        self.create_applications()
        mock_request = MockSearchRequest(name="Wock")

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '26b0a49b-160f-4a8b-b3df-e888092c77e9')

    @tag('integration')
    def test_search_multiple_app_name(self):
        """
        Test to search for a name with two results.
        """
        self.create_applications()
        mock_request = MockSearchRequest(name="Peter")

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 2)
        self.assertTrue(str(response.data[0]['application_id']) == '1e4f8ae7-bf96-497e-bf02-ebe97afb58c5')
        self.assertTrue(str(response.data[1]['application_id']) == '26b0a49b-160f-4a8b-b3df-e888092c77e9')

        ## Date Of Birth Tests

    @tag('integration')
    def test_search_single_app_date_of_birth_one_string(self):
        """
        Test to search for a date_of_birth with one part of the full date.
        """
        self.create_applications()
        mock_request = MockSearchRequest(date_of_birth="04")

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '1e4f8ae7-bf96-497e-bf02-ebe97afb58c5')

    @tag('integration')
    def test_search_single_app_date_of_birth_two_strings(self):
        """
        Test to search for a date_of_birth with two parts of the full date.
        """
        self.create_applications()
        mock_request = MockSearchRequest(date_of_birth="06/03")

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '24e6a689-5434-40a0-80d2-bab6e121fcaa')

    @tag('integration')
    def test_search_single_app_date_of_birth_three_strings(self):
        """
        Test to search for a date_of_birth with a full date.
        """
        self.create_applications()
        mock_request = MockSearchRequest(date_of_birth="03/04/2002")

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '1e4f8ae7-bf96-497e-bf02-ebe97afb58c5')

        ## Home Postcode Tests

    @tag('integration')
    def test_search_single_app_home_postcode(self):
        """
        Test to search for a home_postcode.
        """
        self.create_applications()
        mock_request = MockSearchRequest(home_postcode='CM21 9EP')

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '26b0a49b-160f-4a8b-b3df-e888092c77e9')

        ## Care Location Postcode Tests

    @tag('integration')
    def test_search_single_app_care_location_postcode(self):
        """
        Test to search for a care_location.
        """
        self.create_applications()
        mock_request = MockSearchRequest(care_location_postcode='SW1X 0EP')

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '24e6a689-5434-40a0-80d2-bab6e121fcaa')

        ## Application Reference Tests

    @tag('integration')
    def test_search_single_app_reference(self):
        """
        Test to search for an application_reference number.
        """
        self.create_applications()
        mock_request = MockSearchRequest(application_reference='NA0000001')

        response = ArcSearchListView().list(mock_request)

        self.assertTrue(len(response.data) == 1)
        self.assertTrue(str(response.data[0]['application_id']) == '1e4f8ae7-bf96-497e-bf02-ebe97afb58c5')
