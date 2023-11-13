from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from metrics.services import MetricsService


@method_decorator(csrf_exempt, name='dispatch')
class AverageView(View):
    """
    A view for handling requests related to metric averages.

    Supports retrieving averages based on a specified time interval.
    """
    def get(self, request, *args, **kwargs):
        """
        Get metric averages based on a specified time interval.

        Parameters:
        - request (HttpRequest): The HTTP request.
        
        Returns:
        - JsonResponse: A JSON response containing metric averages.
        """
        interval = request.GET.get('interval', None)
        if interval:
            averages = MetricsService.calculate_averages(interval)
            return JsonResponse(averages, safe=False)

        return JsonResponse({'error': 'Interval parameter is required'}, status=400)
