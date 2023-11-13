from django.db import models


class Metric(models.Model):
    """
    A model representing a metric with timestamp, name, value, created_at, and updated_at.

    Attributes:
        timestamp (DateTimeField): The timestamp when the metric was recorded.
        name (CharField): The name or type of the metric.
        value (FloatField): The numerical value associated with the metric.
        created_at (DateTimeField): The timestamp when the metric record was created.
        updated_at (DateTimeField): The timestamp when the metric record was last updated.

    Methods:
        __str__(): Returns a human-readable string representation of the metric.
    """

    timestamp = models.DateTimeField()
    name = models.CharField(max_length=255)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.name}: {self.value}"
