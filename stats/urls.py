from django.urls import path
from .views import AverageView


urlpatterns = [
    path('averages/', AverageView.as_view(), name='metrics-averages'),
]
