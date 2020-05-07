from django.conf import settings
from django.db import models


class Subscription(models.Model):
    RENEWAL_DAYS = (
        (30, "Every 30 days"),
        (60, "Every 60 days"),
        (90, "Every 90 days"),
        (120, "Every 120 days"),
        (150, "Every 150 days"),
        (180, "Every 180 days"),
    )

    title = models.CharField(max_length=100, blank=False)
    price = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00, blank=False
    )
    start_date = models.DateField(blank=False)
    renewal_cycle_days = models.IntegerField(choices=RENEWAL_DAYS, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
