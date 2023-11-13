import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Metric


@method_decorator(csrf_exempt, name='dispatch')
class MetricView(View):
    """
    A view for handling Metric-related operations.

    Supports creating, updating, retrieving, and deleting metrics.
    """
    def post(self, request, *args, **kwargs):
        """
        Create a new metric.

        Parameters:
        - request (HttpRequest): The HTTP request.
        
        Returns:
        - JsonResponse: A JSON response containing the newly created metric's details.
        """
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
        """
        Get a list of all metrics or retrieve a single metric by ID.

        Parameters:
        - request (HttpRequest): The HTTP request.
        
        Returns:
        - JsonResponse: A JSON response containing the list of metrics or details of a single metric.
        """
        metric_id = kwargs.get('metric_id')
        if metric_id:
            return self.get_single_metric(request, metric_id)
        
        return self.get_metrics(request)

    def get_metrics(self, request):
        """
        Get a list of all metrics.

        Parameters:
        - request (HttpRequest): The HTTP request.
        
        Returns:
        - JsonResponse: A JSON response containing the list of metrics.
        """
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

    def get_single_metric(self, request, metric_id):
        """
        Get details of a single metric by ID.

        Parameters:
        - request (HttpRequest): The HTTP request.
        - metric_id (int): The ID of the metric to retrieve.
        
        Returns:
        - JsonResponse: A JSON response containing the details of the specified metric.
        """
        try:
            metric = Metric.objects.get(id=metric_id)
            
            response_data = {
            "id": metric.id,
            "timestamp": metric.timestamp,
            "name": metric.name,
            "value": metric.value,
            "created_at": metric.created_at,
            "updated_at": metric.updated_at,
            }

            return JsonResponse(response_data)

        except Metric.DoesNotExist:
            return JsonResponse({"error": "Metric not found"}, status=404)

    def put(self, request, metric_id, *args, **kwargs):
        """
        Update an existing metric.

        Parameters:
        - request (HttpRequest): The HTTP request.
        - metric_id (int): The ID of the metric to update.
        
        Returns:
        - JsonResponse: A JSON response containing the updated metric's details.
        """
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
        """
        Delete an existing metric.

        Parameters:
        - request (HttpRequest): The HTTP request.
        - metric_id (int): The ID of the metric to delete.
        
        Returns:
        - JsonResponse: A JSON response indicating the success of the deletion.
        """
        try:
            metric = Metric.objects.get(id=metric_id)
        except Metric.DoesNotExist:
            return JsonResponse({"error": "Metric not found"}, status=404)

        metric.delete()

        return JsonResponse({"message": "Metric deleted successfully"})
