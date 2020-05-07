from rest_framework import generics

from app.permissions import IsCreator

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseList(generics.ListCreateAPIView):
    """
    Lists and creates tasks.
    """

    serializer_class = ExpenseSerializer
    permission_classes = (IsCreator,)

    # Ensure a user sees only own Expense objects.
    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(created_by=user)

    # Set user as owner of a Expense object.
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns a single Expense and allows updates and deletion of a Task
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (IsCreator,)
    lookup_url_kwarg = "expense_id"
