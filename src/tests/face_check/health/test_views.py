from django import test
from django.urls import reverse


class StatusViewTest(test.TestCase):
    def test_status(self):
        response = self.client.get(reverse('health:status'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')


class HealthViewTest(StatusViewTest):
    """
    HealthView test case
    """
