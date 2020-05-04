from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from account.views import LogInView, SignUpView
from expense.views import ExpenseDetail, ExpenseList

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/expense/<int:expense_id>", ExpenseDetail.as_view(), name="expense_detail"
    ),
    path("api/expense/", ExpenseList.as_view(), name="expense"),
    path("api/sign_up/", SignUpView.as_view(), name="sign_up"),
    path("api/log_in/", LogInView.as_view(), name="log_in"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
