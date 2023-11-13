from django.db.models.functions import TruncMinute, TruncHour, TruncDay
from django.db.models import Avg
from .models import Metric


class MetricsService:
    """
    A service class for calculating averages of metrics based on specified time intervals.
    """

    INTERVAL_MAPPING = {
        'minute': TruncMinute,
        'hour': TruncHour,
        'day': TruncDay,
    }

    @staticmethod
    def calculate_averages(interval):
        """
        Calculate average values of metrics based on the specified time interval.

        Parameters:
        - interval (str): The time interval for grouping metrics ('minute', 'hour', or 'day').

        Returns:
        - list: A list of dictionaries containing 'time_interval' and 'average_value' keys.
        """
        grouping = MetricsService.INTERVAL_MAPPING.get(interval)
        if not grouping:
            raise ValueError('Invalid interval')

        metrics = Metric.objects.annotate(
            time_interval=grouping('timestamp')
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
