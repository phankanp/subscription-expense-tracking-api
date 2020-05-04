from django.conf import settings
from django.db import models


class Expense(models.Model):
    title = models.CharField(max_length=500, blank=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, blank=False
    )
    category = models.CharField(max_length=30, blank=False)
    incurred_on = models.DateField(blank=False)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    file = models.FileField(null=True)

    def __str__(self):
        return f"{self.title}"
