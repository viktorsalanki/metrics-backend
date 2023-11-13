import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from metrics.services import MetricsService


@method_decorator(csrf_exempt, name='dispatch')
class AverageView(View):
    def get(self, request, *args, **kwargs):
        interval = request.GET.get('interval', None)
        if interval:
            averages = MetricsService.calculate_averages(interval)
            return JsonResponse(averages, safe=False)
        else:
            return JsonResponse({'error': 'Interval parameter is required'}, status=400)
