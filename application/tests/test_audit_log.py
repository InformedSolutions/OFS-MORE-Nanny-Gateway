from django.conf import settings
from django.test import TestCase

from rest_framework.test import APIRequestFactory, RequestsClient
from timeline_logger.models import TimelineLog

from application import models


class NannyAuditLogsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(NannyAuditLogsTests, cls).setUpClass()
        cls.client = RequestsClient()

    def test_creating_application_creates_timeline_log(self):
        application = models.NannyApplication.objects.create()
        timeline_qset = TimelineLog.objects.filter(object_id=application.pk)

        self.assertTrue(timeline_qset.exists())
        self.assertEqual(timeline_qset[0].extra_data['action'], 'created by')
        self.assertEqual(len(timeline_qset), 1)

    def test_submitting_application_creates_timeline_log(self):
        application = models.NannyApplication.objects.create(application_status='DRAFTING')
        application.application_status = 'SUBMITTED'
        application.save()

        timeline_qset = TimelineLog.objects.filter(object_id=application.pk)

        self.assertTrue(timeline_qset.exists())
        self.assertEqual(timeline_qset[1].extra_data['action'], 'submitted by')
        self.assertEqual(len(timeline_qset), 2)

    def test_resubmitting_application_creates_timeline_log(self):
        application = models.NannyApplication.objects.create(application_status='FURTHER_INFORMATION')
        application.application_status = 'SUBMITTED'
        application.save()

        timeline_qset = TimelineLog.objects.filter(object_id=application.pk)

        self.assertTrue(timeline_qset.exists())
        self.assertEqual(timeline_qset[1].extra_data['action'], 'resubmitted by')
        self.assertEqual(len(timeline_qset), 2)

    def test_returning_application_creates_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_accepting_application_creates_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_post_request_to_arc_comments_endpoint_creates_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_all_models_are_tracked_by_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_user_updating_a_flagged_field_creates_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_duplicate_log_not_added_if_arc_comment_changed(self):
        self.skipTest('NotImplemented')

    def test_resubmitted_application_can_have_same_field_flagged_and_creates_another_timeline_log(self):
        self.skipTest('NotImplemented')

    def test_post_to_timeline_log_endpoint_creates_timeline_log(self):
        response = self.client.post(
            settings.PUBLIC_APPLICATION_URL + '/api/v1/timeline-log/',
            data={
                'object_id': '3141592654',
            }
        )

        timeline_qset = TimelineLog.objects.filter(object_id='3141592654')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(timeline_qset.exists())

    def test_list_request_to_timeline_log_endpoint_returns_associated_timeline_logs_only(self):
        instance_1 = models.NannyApplication.objects.create()
        instance_2 = models.NannyApplication.objects.create()

        response = self.client.get(
            settings.PUBLIC_APPLICATION_URL + '/api/v1/timeline-log/',
            data={
                'object_id': str(instance_1.pk),
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['object_id'], str(instance_1.pk))
