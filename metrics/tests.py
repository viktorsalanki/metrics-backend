import json
from django.test import TestCase
from django.urls import reverse
from .models import Metric


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
        metric = Metric.objects.first()
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
