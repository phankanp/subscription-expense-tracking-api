from django.contrib.auth import get_user_model
from django.core.management import call_command
from datetime import timedelta, datetime
from io import StringIO

from subscription.models import Subscription

import pytest


@pytest.fixture()
def create_user(email="user@example.com", password="pAssw0rd!"):
    """
    Create a test user
    """
    return get_user_model().objects.create_user(
        email=email, first_name="Test", last_name="User", password=password
    )


@pytest.fixture()
def add_subscription():
    """
    Create a test subscription object
    """

    def _add_subscription(title, price, start_date, renewal_cycle_days, created_by):
        subscription = Subscription.objects.create(
            title=title,
            price=price,
            start_date=start_date,
            renewal_cycle_days=renewal_cycle_days,
            created_by=created_by,
        )
        return subscription

    return _add_subscription


@pytest.mark.django_db
class TestEmailReminder:
    def test_command_output_one_week_away(self, create_user, add_subscription):
        date_now = datetime.now()
        date_one_week = date_now + timedelta(weeks=1)

        user = create_user

        add_subscription(
            title="Spotify",
            price="9.99",
            start_date=date_one_week,
            renewal_cycle_days=30,
            created_by=user,
        )

        out = StringIO()
        call_command("email_reminder", stdout=out)
        assert out.getvalue() == "E-mail Report was sent.\n"

    def test_command_output_two_days_away(self, create_user, add_subscription):
        date_now = datetime.now()
        date_two_days = date_now + timedelta(days=2)

        user = create_user

        add_subscription(
            title="Spotify",
            price="9.99",
            start_date=date_two_days,
            renewal_cycle_days=30,
            created_by=user,
        )

        out = StringIO()
        call_command("email_reminder", stdout=out)
        assert out.getvalue() == "E-mail Report was sent.\n"
