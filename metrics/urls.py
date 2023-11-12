from django.urls import path
from .views import MetricView


urlpatterns = [
    path('', MetricView.as_view(), name='metrics-list'),
    path('<int:metric_id>/', MetricView.as_view(), name='metrics-detail'),
]
