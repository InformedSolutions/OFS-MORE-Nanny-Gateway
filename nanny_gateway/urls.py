"""nanny_gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import re

from django.conf.urls import url, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from application import views


schema_view = get_swagger_view(title='OFS-MORE Nanny Gateway')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/v1/first-aid', views.FirstAidViewSet)
router.register(r'api/v1/application', views.NannyApplicationViewSet)
router.register(r'api/v1/childcare-training', views.ChildcareTrainingViewSet)
router.register(r'api/v1/childcare-address', views.ChildcareAddressViewSet)
router.register(r'api/v1/dbs-check', views.DbsViewSet)
router.register(r'api/v1/applicant-personal-details', views.ApplicantPersonalDetailsViewSet)
router.register(r'api/v1/applicant-home-address', views.ApplicantHomeAddressViewSet)
router.register(r'api/v1/insurance-cover', views.InsuranceCoverViewSet)
router.register(r'api/v1/declaration', views.DeclarationViewSet)
router.register(r'api/v1/payment', views.PaymentViewSet)
router.register(r'api/v1/arc-comments', views.ArcCommentsViewSet)
router.register(r'api/v1/timeline-log', views.TimeLineLogViewSet)
router.register(r'api/v1/arc-search', views.ArcSearchListView)



urlpatterns = [
    url(r'^api/v1/summary/(?P<name>\w+)/(?P<application_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.summary_table, name="Summary"),
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api/v1/application/application_reference/(?P<application_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        views.retrieve_reference_number, name='Assign-Application-Reference-View'),
]


if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern

handler404 = views.yield404