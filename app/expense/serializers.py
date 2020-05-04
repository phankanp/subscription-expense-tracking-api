from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("id", "title", "amount", "category", "incurred_on", "notes", "file")

        extra_kwargs = {
            "created_by": {"read_only": True},
            "updated": {"read_only": True},
        }
