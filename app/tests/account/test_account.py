from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status

import base64
import json

import pytest


PASSWORD = "pAssw0rd!"


@pytest.fixture()
def create_user(email="user@example.com", password=PASSWORD):
    return get_user_model().objects.create_user(
        email=email, first_name="Test", last_name="User", password=password
    )


@pytest.mark.django_db
class TestAuthentication:
    def test_user_can_sign_up(self, client):
        response = client.post(
            reverse("sign_up"),
            data={
                "email": "user@example.com",
                "first_name": "Test",
                "last_name": "User",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        user = get_user_model().objects.last()
        assert status.HTTP_201_CREATED == response.status_code
        assert response.data["id"] == user.id
        assert response.data["email"] == user.email
        assert response.data["first_name"] == user.first_name
        assert response.data["last_name"] == user.last_name

    def test_user_can_log_in(self, client, create_user):
        user = create_user
        response = client.post(
            reverse("log_in"), data={"email": user.email, "password": PASSWORD, }
        )

        access = response.data["access"]
        header, payload, signature = access.split(".")
        decoded_payload = base64.b64decode(f"{payload}==")
        payload_data = json.loads(decoded_payload)

        assert status.HTTP_200_OK == response.status_code
        assert response.data["refresh"]
        assert payload_data["user_id"] == user.id
        assert payload_data["email"] == user.email
        assert payload_data["first_name"] == user.first_name
        assert payload_data["last_name"] == user.last_name
