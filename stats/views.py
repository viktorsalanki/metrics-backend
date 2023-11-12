from django.db.models.functions import TruncMinute, TruncHour, TruncDay
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from metrics.models import Metric


@method_decorator(csrf_exempt, name='dispatch')
class AverageView(View):
    def get(self, request, *args, **kwargs):
        interval = request.GET.get('interval', None)
        if interval:
            return self.get_averages(request, interval)
        else:
            return JsonResponse({'error': 'Interval parameter is required'}, status=400)

    def get_averages(self, request, interval):
        if interval == 'minute':
            grouping = TruncMinute('timestamp')
        elif interval == 'hour':
            grouping = TruncHour('timestamp')
        elif interval == 'day':
            grouping = TruncDay('timestamp')
        else:
            return JsonResponse({'error': 'Invalid interval'}, status=400)

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

        return JsonResponse(response_data, safe=False)
