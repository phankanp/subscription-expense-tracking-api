from django.contrib import admin
from django.urls import path

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from account.views import LogInView, SignUpView
from expense.views import ExpenseDetail, ExpenseList
from subscription.views import SubscriptionDetail, SubscriptionList

schema_view = get_schema_view(
    openapi.Info(
        title="Subscription/Expense Tracking API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/subscription/<int:subscription_id>",
        SubscriptionDetail.as_view(),
        name="subscription_detail",
    ),
    path("api/subscription/", SubscriptionList.as_view(), name="subscription"),
    path(
        "api/expense/<int:expense_id>", ExpenseDetail.as_view(), name="expense_detail"
    ),
    path("api/expense/", ExpenseList.as_view(), name="expense"),
    path("api/sign_up/", SignUpView.as_view(), name="sign_up"),
    path("api/log_in/", LogInView.as_view(), name="log_in"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("swagger-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
