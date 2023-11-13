import json
from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from django.urls import reverse
from metrics.services import MetricsService
from stats.views import AverageView


class MockMetricsService(MetricsService):
    @staticmethod
    def calculate_averages(interval):
        return [{'time_interval': '2023-11-10T12:00:00+00:00', 'average_value': 42.0}]


class AverageViewTests(TestCase):

    @patch('metrics.services.MetricsService.calculate_averages', MockMetricsService.calculate_averages)
    def test_get_averages_minute(self):
        request_factory = RequestFactory()
        request = request_factory.get('api/v1/stats/averages/?interval=minute')
        view = AverageView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        data = json.loads(response.content.decode('utf-8'))

        self.assertIn('time_interval', data[0])
        self.assertIn('average_value', data[0])
        self.assertEqual(42.0, data[0]['average_value'])

    def test_get_averages_missing_interval(self):
        url = reverse('metrics-averages')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Interval parameter is required')
