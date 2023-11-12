from django.urls import path
from .views import MetricView


urlpatterns = [
    path('metrics/', MetricView.as_view(), name='metrics-list'),
    path('metrics/<int:metric_id>/', MetricView.as_view(), name='metrics-detail'),
]
