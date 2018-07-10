from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view
from django.http import JsonResponse

from application.models.nanny_models.dbs_check import DbsCheckSerializer, DbsCheck
from application.models.nanny_models.nanny_application import NannyApplication, NannyApplicationSerializer
from application.models import FirstAidTraining, FirstAidTrainingSerializer
from application.models.nanny_models.childcare_training import ChildcareTraining, ChildcareTrainingSerializer
from application.models.nanny_models.childcare_address import ChildcareAddress, ChildcareAddressSerializer
from application.models.nanny_models.applicant_personal_details import ApplicantPersonalDetails, \
    ApplicantPersonalDetailsSerializer
from application.models.nanny_models.applicant_home_address import ApplicantHomeAddress, ApplicantHomeAddressSerializer
from application.models.nanny_models.childcare_training import ChildcareTraining, ChildcareTrainingSerializer
from application.models.nanny_models.insurance_cover import InsuranceCover, InsuranceCoverSerializer
from application.models.nanny_models.declaration import Declaration, DeclarationSerializer

serializers = {'applicant_home_address': ApplicantHomeAddressSerializer,
               'applicant_personal_details': ApplicantPersonalDetailsSerializer,
               'childcare_address': ChildcareAddressSerializer,
               'childcare_training': ChildcareTrainingSerializer,
               'dbs_check': DbsCheckSerializer,
               'first_aid': FirstAidTrainingSerializer,
               'insurance_cover': InsuranceCoverSerializer,
               'application': NannyApplicationSerializer}


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
    queryset = NannyApplication.objects.all()
    serializer_class = NannyApplicationSerializer
    filter_fields = (
        'application_id',
    )


class ChildcareAddressViewSet(BaseViewSet):
    queryset = ChildcareAddress.objects.all()
    serializer_class = ChildcareAddressSerializer
    filter_fields = (
        'childcare_address_id',
        'application_id'
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
        'application_id'
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


@api_view(['GET'])
def summary_table(request, name, application_id):
    if request.method == 'GET':
        if name in serializers.keys():
            serializer = serializers[name]
            model = serializer.Meta.model
            records = model.objects.filter(application_id=application_id)
            if name != "childcare_address":
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
