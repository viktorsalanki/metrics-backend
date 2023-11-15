import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Metric
from .services import MetricsService


class MetricViewTests(TestCase):
    def test_create_metric(self):
        url = reverse('metrics-list')
        data = {
            'timestamp': '2023-11-08T12:00:00+00:00',
            'name': 'temperature',
            'value': 25.5,
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        metric = Metric.objects.last()
        self.assertIsNotNone(metric)
        self.assertEqual(metric.timestamp.isoformat(), data['timestamp'])
        self.assertEqual(metric.name, data['name'])
        self.assertEqual(metric.value, data['value'])

    def test_update_metric(self):
        metric = Metric.objects.create(
            timestamp='2023-11-08T12:00:00+00:00',
            name='pressure',
            value=1013.25
        )

        url = reverse('metrics-detail', args=[metric.id])
        data = {
            'timestamp': '2023-11-08T14:00:00+00:00',
            'name': 'pressure',
            'value': 1014.5,
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        updated_metric = Metric.objects.get(id=metric.id)
        self.assertEqual(updated_metric.timestamp.isoformat(), data['timestamp'])
        self.assertEqual(updated_metric.name, data['name'])
        self.assertEqual(updated_metric.value, data['value'])

    def test_delete_metric(self):
        metric = Metric.objects.create(
            timestamp='2023-11-08T12:00:00+00:00',
            name='wind_speed',
            value=15.0
        )

        url = reverse('metrics-detail', args=[metric.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Metric.DoesNotExist):
            Metric.objects.get(id=metric.id)

    def test_get_single_metric(self):
        metric = Metric.objects.create(
            timestamp='2023-11-08T12:00:00Z',
            name='pressure',
            value=1013.25
        )

        url = reverse('metrics-detail', args=[metric.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data['id'], metric.id)
        self.assertEqual(data['timestamp'], '2023-11-08T12:00:00Z')
        self.assertEqual(data['name'], metric.name)
        self.assertEqual(data['value'], metric.value)

    def test_get_single_metric_not_found(self):
        invalid_id = 999
        url = reverse('metrics-detail', args=[invalid_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Metric not found')


class MetricServicesTests(TestCase):
    def setUp(self):
        Metric.objects.create(timestamp=timezone.now(), name='temperature', value=20.0)
        Metric.objects.create(timestamp=timezone.now(), name='temperature', value=30.0)

    def test_calculate_averages_minute(self):
        metrics_service = MetricsService()

        averages = metrics_service.calculate_averages('minute')

        self.assertIn('time_interval', averages[-1])
        self.assertIn('temperature', averages[-1])
        self.assertEqual(averages[-1]['temperature'], 25.0)

    def test_calculate_averages_hour(self):
        metrics_service = MetricsService()

        averages = metrics_service.calculate_averages('hour')

        self.assertIn('time_interval', averages[-1])
        self.assertIn('temperature', averages[-1])
        self.assertEqual(averages[-1]['temperature'], 25.0)

    def test_calculate_averages_day(self):
        metrics_service = MetricsService()

        averages = metrics_service.calculate_averages('day')

        self.assertIn('time_interval', averages[-1])
        self.assertIn('temperature', averages[-1])
        self.assertEqual(averages[-1]['temperature'], 25.0)

    def test_calculate_averages_invalid_interval(self):
        metrics_service = MetricsService()

        with self.assertRaises(ValueError):
            metrics_service.calculate_averages('invalid_interval')
