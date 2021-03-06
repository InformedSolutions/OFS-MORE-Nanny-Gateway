import logging

from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import (ApplicantHomeAddress, ApplicantHomeAddressSerializer, ApplicantPersonalDetails,
                     ApplicantPersonalDetailsSerializer, ArcComments, ArcCommentsSerializer, ChildcareAddress,
                     ChildcareAddressSerializer, ChildcareTraining, ChildcareTrainingSerializer, DbsCheckSerializer,
                     DbsCheck, Declaration, DeclarationSerializer, InsuranceCover, InsuranceCoverSerializer,
                     NannyApplication, NannyApplicationSerializer, TimelineLog, TimelineLogSerializer,
                     FirstAidTraining, FirstAidTrainingSerializer, Payment, PaymentSerializer,
                     ApplicantChildrenDetailsSerializer, NannyPreviousRegistrationDetails,
                     PreviousRegistrationSerializer, PreviousAddress, PreviousAddressSerializer,
                     NannyPreviousName, PreviousNameSerializer)
from .query_nannies import get_nannies_query
from .your_children_table import get_your_children_header_table
from .services import noo_integration_service


serializers = {'applicant_home_address': ApplicantHomeAddressSerializer,
               'applicant_personal_details': ApplicantPersonalDetailsSerializer,
               'childcare_address': ChildcareAddressSerializer,
               'childcare_training': ChildcareTrainingSerializer,
               'dbs_check': DbsCheckSerializer,
               'first_aid': FirstAidTrainingSerializer,
               'insurance_cover': InsuranceCoverSerializer,
               'application': NannyApplicationSerializer,
               'arc_comments': ArcCommentsSerializer,
               'your_children': ApplicantChildrenDetailsSerializer,
               'nanny-previous-registration-details': PreviousRegistrationSerializer,
               'previous-address': PreviousAddressSerializer,
               }

logger = logging.getLogger(__name__)


class BaseViewSet(viewsets.ModelViewSet):
    """
    list:
    List all current applications stored in the database
    create:
    Create a new full application in the database
    retrieve:
    List the application with the corresponding primary key (application_id) from the database
    update:
    Update all fields in a record with the corresponding primary key (application_id) from the database
    partial_update:
    Update any amount of fields in  a record with the corresponding primary key (application_id) from the database
    destroy:
    Delete the application with the corresponding primary key (application_id) from the database
    """
    lookup_field = 'application_id'
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if not queryset.exists():
            raise NotFound(detail="Error 404, resource not found", code=404)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NannyApplicationViewSet(BaseViewSet):

    # custom filter to allow range filtering on last-accessed date
    class ApplicationFilter(filters.FilterSet):
        last_accessed_before = filters.IsoDateTimeFilter('date_last_accessed', lookup_expr='lt')
        last_accessed_after = filters.IsoDateTimeFilter('date_last_accessed', lookup_expr='gt')

        class Meta:
            model = NannyApplication
            fields = ['application_id', 'application_status', 'last_accessed_before', 'last_accessed_after']

    queryset = NannyApplication.objects.all()
    serializer_class = NannyApplicationSerializer
    filter_class = ApplicationFilter


class ChildcareAddressViewSet(BaseViewSet):
    lookup_field = 'pk'
    queryset = ChildcareAddress.objects.all()
    serializer_class = ChildcareAddressSerializer
    filter_fields = (
        'childcare_address_id',
        'application_id',
        'street_line1',
        'street_line2',
        'town',
        'county',
        'country',
        'postcode'
    )
    ordering_fields = (
        'date_created'
    )
    ordering = (
        'date_created',
    )


class ChildcareTrainingViewSet(BaseViewSet):
    queryset = ChildcareTraining.objects.all()
    serializer_class = ChildcareTrainingSerializer
    filter_fields = (
        'application_id',
    )


class FirstAidViewSet(BaseViewSet):
    queryset = FirstAidTraining.objects.all()
    serializer_class = FirstAidTrainingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'first_aid_id',
        'application_id',
    )


class DbsViewSet(BaseViewSet):
    queryset = DbsCheck.objects.all()
    serializer_class = DbsCheckSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = (
        'dbs_id',
        'application_id'
    )


class ApplicantPersonalDetailsViewSet(BaseViewSet):
    queryset = ApplicantPersonalDetails.objects.all()
    serializer_class = ApplicantPersonalDetailsSerializer
    filter_fields = (
        'personal_detail_id',
        'application_id'
    )


class ApplicantHomeAddressViewSet(BaseViewSet):
    queryset = ApplicantHomeAddress.objects.all()
    serializer_class = ApplicantHomeAddressSerializer
    filter_fields = (
        'home_address_id',
        'personal_detail_id',
        'application_id',
    )


class PreviousAddressViewSet(BaseViewSet):
    lookup_field = 'pk'
    queryset = PreviousAddress.objects.all().order_by('order')
    serializer_class = PreviousAddressSerializer
    filter_fields = (
        'previous_address_id',
        'person_id',
        'person_type',
    )


class InsuranceCoverViewSet(BaseViewSet):
    queryset = InsuranceCover.objects.all()
    serializer_class = InsuranceCoverSerializer
    filter_fields = (
        'insurance_cover_id',
        'application_id'
    )


class DeclarationViewSet(BaseViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    filter_fields = (
        'declaration_id',
        'application_id'
    )


class PaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_fields = (
        'payment_id',
        'application_id'
    )


class ArcCommentsViewSet(BaseViewSet):
    lookup_field = 'review_id'
    queryset = ArcComments.objects.all()
    serializer_class = ArcCommentsSerializer
    filter_fields = (
        'review_id',
        'table_pk',
        'field_name',
        'application_id',
        'endpoint_name',
    )


class PreviousRegistrationViewSet(BaseViewSet):
    queryset = NannyPreviousRegistrationDetails.objects.all()
    serializer_class = PreviousRegistrationSerializer
    filter_fields = (
        'application_id',
        'previous_registration',
        'individual_id',
        'five_years_in_UK',
    )

class PreviousNameViewSet(BaseViewSet):
    lookup_field = 'previous_name_id'
    queryset = NannyPreviousName.objects.all()
    serializer_class = PreviousNameSerializer
    filter_fields = (
        'application_id',
        'previous_name_id'
    )

class ArcSearchListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A viewset containing a list() function.
    Implemented to allow for search queries on the Nanny DB.
    """
    queryset = NannyApplication.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Returns a list of dictionaries containing information for populating the Arc search table.
        The following is a list of optional parameters:
        name --- Applicant's name, referring to either their first or last name.
        date_of_birth --- Applicant's date of birth
        home_postcode --- Applicant's home postcode
        care_location_postcode --- Any of the applicant's care location's postcode.
        application_reference --- Application's reference, beginning 'NA'.
        """
        query_params = self.__get_query_params(request)
        nannies_queryset = self.__query_nannies(*query_params)

        response_dict = [
            {'application_id': query.application_id,
             'application_reference': query.application_reference,
             'application_type': 'Nanny',
             'applicant_name': self.__get_applicant_name(query.application_id),
             'date_submitted': self.__format_date(query.date_submitted),
             'date_accessed': self.__format_date(query.date_updated),
             'submission_type': query.application_status}
            for query in nannies_queryset]

        return Response(response_dict)

    @staticmethod
    def __get_applicant_name(app_id):
        """
        Returns an applicant's first_name, last_name
        :param app_id: Applicant's id
        :return: String
        """
        if ApplicantPersonalDetails.objects.filter(application_id=app_id).exists():
            applicant_person_details_record = ApplicantPersonalDetails.objects.get(application_id=app_id)

            first_name = applicant_person_details_record.first_name
            last_name = applicant_person_details_record.last_name

            return "{0} {1}".format(first_name, last_name)

        else:
            return ""

    @staticmethod
    def __format_date(datetime) -> str:
        """
        Converts datetime to string in displayable format DD/MM/YYYY
        :param datetime: datetime object or None
        :return: String
        """
        if datetime:
            return datetime.strftime('%d/%m/%Y')
        else:
            return ""

    @staticmethod
    def __get_query_params(request):
        """
        Extracts specific information from the request query_params.
        :param request: request object, containing query_params.
        :return: Tuple of sent data.
        """
        name = request.query_params.get('name')
        date_of_birth = request.query_params.get('date_of_birth')
        home_postcode = request.query_params.get('home_postcode')
        care_location_postcode = request.query_params.get('care_location_postcode')
        application_reference = request.query_params.get('application_reference')

        return name, date_of_birth, home_postcode, care_location_postcode, application_reference

    @staticmethod
    def __query_nannies(name, date_of_birth, home_postcode, care_location_postcode, application_reference):
        """
        Calls get_nannies_query, an external function that constructs a Q object.
        :return: A filtered NannyApplication queryset
        """
        query = get_nannies_query(name, date_of_birth, home_postcode, care_location_postcode, application_reference)

        return NannyApplication.objects.filter(query)


class TimeLineLogViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = TimelineLog.objects.all().order_by('-timestamp')
    serializer_class = TimelineLogSerializer
    filter_fields = (
        'object_id',
    )


@api_view(['GET'])
def summary_table(request, name, application_id):
    if request.method == 'GET':
        if name in serializers.keys():
            serializer = serializers[name]
            model = serializer.Meta.model
            records = model.objects.filter(application_id=application_id)

            if name == 'your_children':
                response_header_table = [get_your_children_header_table(records)]

                # The records list is reversed due to the order in which the records are pulled from the
                # database being reversed.
                response_child_tables = [serializer(record).get_summary_table() for record in
                                         reversed(records)]

                response = response_header_table + response_child_tables

                return JsonResponse(response, safe=False)

            elif name != "childcare_address":
                if records:
                    return JsonResponse(serializer(records[0]).get_summary_table(), safe=False)
                else:
                    return JsonResponse([], safe=False)
            else:
                summary_list = []
                i = 1
                summary_list.append(serializer().get_title_row())
                for record in records:
                    row = serializer(record).get_summary_table(i)
                    summary_list.append(row)
                    i += 1
                return JsonResponse(summary_list, safe=False)


@api_view(['GET'])
def retrieve_reference_number(request, application_id):
    """
    Method for allocating a reference number to an application
    or retrieving an existing reference number
    """
    try:
        application = NannyApplication.objects.get(pk=application_id)

        # If an application reference number has not yet been allocated
        # assign an persist value
        try:
            if application.application_reference is None:
                application.application_reference = noo_integration_service.create_application_reference()
                application.save()

            return JsonResponse({
                'reference': application.application_reference
            })
        except Exception as e:
            logger.error('Failed to allocate application reference number: ' + str(e))
            return yield503(request)
    except NannyApplication.DoesNotExist:
        return yield404(request)


@api_view(['POST'])
def send_payment_notification(request):
    """
    Method for sending a payment notification to Amazon SQS.
    ---
    Parameters in the POST body must include application_id (string) and amount (int)
    """
    try:

        application_id = request.data.get('application_id')
        amount = request.data.get('amount')

        # Check application exists
        NannyApplication.objects.get(pk=application_id)

        try:
            noo_integration_service.send_payment_notification(application_id, amount)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error('Failed to dispatch payment notification request: ' + str(e))
            return yield503(request)
    except NannyApplication.DoesNotExist:
        return yield404(request)


def yield404(request):
    """
    Custom handler to yield a JSON object with a 404 status code
    :param request: the inbound HTTP request
    :return: An http response comprised of a descriptive error and a 404 status code
    """
    return Response({
        'error': 'The resource was not found'
    }, status=status.HTTP_404_NOT_FOUND)


def yield503(request):
    """
    Custom handler to yield a JSON object with a 503 status code
    :param request: the inbound HTTP request
    :return: An http response comprised of a descriptive error and a 404 status code
    """
    return Response({
        'error': 'The service was unavailable'
    }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
