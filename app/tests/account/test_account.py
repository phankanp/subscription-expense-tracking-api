from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework import status

from expense.models import Expense
from account.serializers import UserSerializer

import base64
import json

import pytest


PASSWORD = "pAssw0rd!"


@pytest.fixture()
def create_user(email="user@example.com", password=PASSWORD):
    """
    Creates a new user
    """
    return get_user_model().objects.create_user(
        email=email, first_name="Test", last_name="User", password=password
    )


@pytest.mark.django_db
class TestAuthentication:
    def test_user_can_sign_up(self, client):
        """
        Test for user registration
        """
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
        assert user.get_full_name() == f"{user.first_name} {user.last_name}"
        assert str(user) == f"{user.get_full_name()} <{user.email}>"
        assert user.has_perm("Yes") is True
        assert user.has_module_perms(Expense) is True

    def test_user_can_sign_up_mismatch_password_serializer(self, client):
        """
        Test for user serializer with mistmatch password
        """
        invalid_serializer_data = {
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": PASSWORD,
            "password2": "mismatchPassword",
        }

        serializer = UserSerializer(data=invalid_serializer_data)
        assert not serializer.is_valid()

        with pytest.raises(Exception):
            UserSerializer.validate(invalid_serializer_data)

    def test_user_can_log_in(self, client, create_user):
        """
        Test for user login
        """
        user = create_user
        response = client.post(
            reverse("log_in"), data={"email": user.email, "password": PASSWORD}
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

    def test_create_superuser(self, client):
        """
        Test for create superuser
        """
        superuser = get_user_model().objects.create_superuser(
            email="superuser@example.com",
            first_name="SuperTest",
            last_name="User",
            password=PASSWORD,
        )

        assert superuser.email == "superuser@example.com"
        assert superuser.first_name == "SuperTest"
        assert superuser.last_name == "User"
        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.is_active is True

    def test_create_superuser_invalid(self, client):
        """
        Test for superuser is_staff and is_superuser are True
        """
        with pytest.raises(Exception):
            get_user_model().objects.create_superuser(
                email="superuser@example.com",
                first_name="SuperTest",
                last_name="User",
                password=PASSWORD,
                is_staff=False,
                is_superuser=True,
            )

        with pytest.raises(Exception):
            get_user_model().objects.create_superuser(
                email="superuser@example.com",
                first_name="SuperTest",
                last_name="User",
                password=PASSWORD,
                is_staff=True,
                is_superuser=False,
            )

    def test_create_user_invalid(self, client):
        """
        Test for superuser has email, first, and last name
        """
        with pytest.raises(Exception):
            get_user_model().objects.create_user(
                email="", first_name="Test", last_name="User", password=PASSWORD
            )

        with pytest.raises(Exception):
            get_user_model().objects.create_user(
                email="user@example.com",
                first_name="",
                last_name="User",
                password=PASSWORD,
            )

        with pytest.raises(Exception):
            get_user_model().objects.create_user(
                email="user@example.com",
                first_name="Test",
                last_name="",
                password=PASSWORD,
            )
