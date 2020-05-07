from rest_framework import serializers

from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    RENEWAL_DAYS = (30, "60", "90", "120", "150", "180")

    renewal_cycle_days = serializers.ChoiceField(choices=RENEWAL_DAYS)

    class Meta:
        model = Subscription
        fields = ("title", "price", "start_date", "renewal_cycle_days")
