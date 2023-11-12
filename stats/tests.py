import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from metrics.models import Metric


class AverageViewTests(TestCase):
    def setUp(self):
        Metric.objects.create(timestamp=timezone.now(), name='temperature', value=20.0)
        Metric.objects.create(timestamp=timezone.now(), name='temperature', value=30.0)

    def test_get_averages_minute(self):
        url = reverse('metrics-averages') + '?interval=minute'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn('time_interval', data[0])
        self.assertIn('average_value', data[0])

        self.assertIn('T', data[0]['time_interval'])
        self.assertIsInstance(data[0]['average_value'], float)
        self.assertEqual(data[0]['average_value'], 25.0)

    def test_get_averages_invalid_interval(self):
        url = reverse('metrics-averages') + '?interval=invalid'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid interval')
