from itertools import groupby
from operator import itemgetter
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

    FORMAT_MAPPING = {
        'minute': '%Y-%m-%d %H:%M',
        'hour': '%Y-%m-%d %H:00',
        'day': '%Y-%m-%d',
    }

    @staticmethod
    def calculate_averages(interval):
        """
        Calculate average values of metrics based on the specified time interval.

        Parameters:
        - interval (str): The time interval for grouping metrics ('minute', 'hour', or 'day').

        Returns:
        - list: A list of dictionaries containing 'time_interval' and metric names as keys.
        """
        grouping = MetricsService.INTERVAL_MAPPING.get(interval)
        if not grouping:
            raise ValueError('Invalid interval')

        metrics = (
            Metric.objects
            .annotate(time_interval=grouping('timestamp'))
            .values('time_interval', 'name')
            .annotate(average_value=Avg('value'))
            .order_by('time_interval', 'name')
        )

        grouped_metrics = groupby(metrics, key=itemgetter('time_interval'))

        response_data = []

        for time_interval, metrics_group in grouped_metrics:
            entry = {'time_interval': time_interval.strftime(MetricsService.FORMAT_MAPPING[interval])}
            for metric in metrics_group:
                entry[metric['name']] = metric['average_value']
            response_data.append(entry)

        return response_data
