from django.contrib.auth import get_user_model
from subscription.models import Subscription
from rest_framework.reverse import reverse

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
def login_user(client, create_user):
    """
    Login test user and generate JWT response
    """
    user = create_user

    response = client.post(
        reverse("log_in"), data={"email": user.email, "password": "pAssw0rd!"}
    )

    client.login(email=user.email, password="pAssw0rd!")

    return response


@pytest.fixture()
def generate_headers():
    """
    Generate request headers
    """

    def _generate_headers(access):
        headers = {
            "Authorization": "Bearer " + access,
            "content_type": "application/json",
        }
        return headers

    return _generate_headers


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
def test_subscription_model(create_user):
    """
    Test creating subscription model
    """
    user = create_user

    subscription = Subscription(
        title="Spotify",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )
    subscription.save()

    assert subscription.title == "Spotify"
    assert subscription.price == "9.99"
    assert subscription.start_date == "2020-06-01"
    assert subscription.renewal_cycle_days == 30
    assert subscription.updated
    assert subscription.created_by.id == user.id
    assert str(subscription) == subscription.title


@pytest.mark.django_db
def test_add_subscription(client, create_user, login_user, generate_headers):
    """
    Test adding new subscription
    """
    subscription = Subscription.objects.all()
    assert len(subscription) == 0

    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    resp = client.post(
        "/api/subscription/",
        {
            "title": "Netflix",
            "amount": "9.99",
            "start_date": "2020-05-12",
            "renewal_cycle_days": 30,
        },
        headers=headers,
    )

    assert resp.status_code == 201
    assert resp.data["title"] == "Netflix"

    subscription = Subscription.objects.all()
    assert len(subscription) == 1


@pytest.mark.django_db
def test_get_single_subscription(
    client, create_user, login_user, add_subscription, generate_headers
):
    """
    Test get single subscription by id
    """
    user = create_user
    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    subscription = add_subscription(
        title="Spotify",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )

    resp = client.get(f"/api/subscription/{subscription.id}", headers=headers)

    assert resp.status_code == 200
    assert resp.data["title"] == "Spotify"


@pytest.mark.django_db
def test_get_all_subscription(
    client, create_user, login_user, add_subscription, generate_headers
):
    """
    Test get all subscription by user
    """
    user = create_user
    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    subscription_one = add_subscription(
        title="Spotify",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )

    subscription_two = add_subscription(
        title="Netflix",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )

    resp = client.get(f"/api/subscription/", headers=headers)

    assert resp.status_code == 200
    assert resp.data[0]["title"] == subscription_one.title
    assert resp.data[1]["title"] == subscription_two.title


@pytest.mark.django_db
def test_delete_subscription(
    client, create_user, login_user, add_subscription, generate_headers
):
    """
    Test delete subscription by id
    """
    user = create_user
    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    subscription = add_subscription(
        title="Spotify",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )

    resp = client.get(f"/api/subscription/{subscription.id}", headers=headers)

    assert resp.status_code == 200
    assert resp.data["title"] == "Spotify"

    resp_two = client.delete(f"/api/subscription/{subscription.id}", headers=headers)
    assert resp_two.status_code == 204

    resp_three = client.get(f"/api/subscription/", headers=headers)
    assert resp_three.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_update_subscription(
    client, create_user, login_user, add_subscription, generate_headers
):
    """
    Test update subscription
    """
    user = create_user
    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    subscription = add_subscription(
        title="Spotify",
        price="9.99",
        start_date="2020-06-01",
        renewal_cycle_days=30,
        created_by=user,
    )

    resp = client.put(
        f"/api/subscription/{subscription.id}",
        {
            "title": "Netflix",
            "amount": "9.99",
            "start_date": "2020-06-05",
            "renewal_cycle_days": 30,
        },
        headers=headers,
        content_type="application/json",
    )

    assert resp.status_code == 200
    assert resp.data["title"] == "Netflix"
    assert resp.data["start_date"] == "2020-06-05"

    resp_two = client.get(f"/api/subscription/{subscription.id}", headers=headers)
    assert resp_two.status_code == 200
    assert resp_two.data["title"] == "Netflix"
    assert resp_two.data["start_date"] == "2020-06-05"
