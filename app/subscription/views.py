from rest_framework import generics

from app.permissions import IsCreator

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionList(generics.ListCreateAPIView):
    """
    Lists and creates subscriptions.
    """

    serializer_class = SubscriptionSerializer
    permission_classes = (IsCreator,)

    # Ensure a user sees only own Subscription objects.
    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(created_by=user)

    # Set user as owner of a Subscription object.
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns a single subscription and allows updates and deletion of a subscription
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsCreator,)
    lookup_url_kwarg = "subscription_id"
