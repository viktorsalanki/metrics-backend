from django.db.models.functions import TruncMinute, TruncHour, TruncDay
from django.db.models import Avg
from django.http import JsonResponse
from .models import Metric


class MetricsService:
    @staticmethod
    def calculate_averages(interval):
        if interval == 'minute':
            grouping = TruncMinute('timestamp')
        elif interval == 'hour':
            grouping = TruncHour('timestamp')
        elif interval == 'day':
            grouping = TruncDay('timestamp')
        else:
            raise ValueError('Invalid interval')

        metrics = Metric.objects.annotate(
            time_interval=grouping
        ).values('time_interval').annotate(
            average_value=Avg('value')
        ).order_by('time_interval')

        response_data = [
            {
                'time_interval': metric['time_interval'].isoformat(),
                'average_value': metric['average_value'],
            }
            for metric in metrics
        ]

        return response_data
