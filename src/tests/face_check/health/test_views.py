from unittest import mock

from django import test
from django.urls import reverse

from face_check.health import views
from face_check.consts import HttpStatus


class StatusViewTest(test.TestCase):
    def test_ready(self):
        response = self.client.get(reverse('health:status'))
        self.assertEqual(response.status_code, HttpStatus.OK)
        self.assertEqual(response.content, b'ok')


class HealthViewTest(test.TestCase):
    """
    HealthView test case
    """
    def test_health_ok(self):
        response = self.client.get(reverse('health:status'))
        self.assertEqual(response.status_code, HttpStatus.OK)
        self.assertEqual(response.content, b'ok')

    def test_health_database_connection_failure(self):
        with mock.patch('face_check.health.views._app_health_check',
                        side_effect=[views.OperationalError()]):
            response = self.client.get(reverse('health:health'))
            self.assertEqual(response.status_code, HttpStatus.DOWN)
            self.assertEqual(response.content, b'fail')

    def test_health_failure_unknown(self):
        with mock.patch('face_check.health.views._app_health_check',
                        side_effect=[Exception()]):
            response = self.client.get(reverse('health:health'))
            self.assertEqual(response.status_code, HttpStatus.DOWN)
            self.assertEqual(response.content, b'fail <unhandled exception>')
