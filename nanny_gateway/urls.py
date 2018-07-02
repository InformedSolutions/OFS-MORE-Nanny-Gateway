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
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from application import views

schema_view = get_swagger_view(title='OFS-MORE Nanny Gateway')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/v1/first_aid_training', views.FirstAidViewSet)
router.register(r'api/v1/application', views.NannyApplicationViewSet)
router.register(r'api/v1/childcare-training', views.ChildcareTrainingViewSet)
router.register(r'api/v1/childcare-address', views.ChildcareAddressViewSet)
router.register(r'api/v1/dbs-check', views.DbsViewSet)
router.register(r'api/v1/applicant-personal-details', views.ApplicantPersonalDetailsViewSet)
router.register(r'api/v1/applicant-home-address', views.ApplicantHomeAddressViewSet)

urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls))
]


if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern

