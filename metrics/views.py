import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Metric


@method_decorator(csrf_exempt, name='dispatch')
class MetricView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        timestamp = data.get('timestamp')
        name = data.get('name')
        value = data.get('value')

        metric = Metric.objects.create(timestamp=timestamp, name=name, value=value)
        response_data = {
            "message": "Metric created successfully",
            "id": metric.id,
            "created_at": metric.created_at,
            "updated_at": metric.updated_at,
        }

        return JsonResponse(response_data)

    def get(self, request, *args, **kwargs):
        metrics = Metric.objects.all()
        response_data = [
            {
                "id": metric.id,
                "timestamp": metric.timestamp,
                "name": metric.name,
                "value": metric.value,
                "created_at": metric.created_at,
                "updated_at": metric.updated_at,
            }
            for metric in metrics
        ]
        return JsonResponse(response_data, safe=False)

    def put(self, request, metric_id, *args, **kwargs):
        data = json.loads(request.body)
        try:
            metric = Metric.objects.get(id=metric_id)
        except Metric.DoesNotExist:
            return JsonResponse({"error": "Metric not found"}, status=404)

        metric.timestamp = data.get('timestamp', metric.timestamp)
        metric.name = data.get('name', metric.name)
        metric.value = data.get('value', metric.value)
        metric.save()

        response_data = {
            "message": "Metric updated successfully",
            "id": metric.id,
            "timestamp": metric.timestamp,
            "name": metric.name,
            "value": metric.value,
            "created_at": metric.created_at,
            "updated_at": metric.updated_at,
        }

        return JsonResponse(response_data)

    def delete(self, request, metric_id, *args, **kwargs):
        try:
            metric = Metric.objects.get(id=metric_id)
        except Metric.DoesNotExist:
            return JsonResponse({"error": "Metric not found"}, status=404)

        metric.delete()

        return JsonResponse({"message": "Metric deleted successfully"})
