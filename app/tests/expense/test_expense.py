from django.contrib.auth import get_user_model
from expense.models import Expense
from rest_framework.reverse import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO
from PIL import Image

import pytest
import sys


@pytest.fixture(scope="function")
def image_mock():
    """
    Generate mock image file
    """

    def _image_mock(num):
        file = BytesIO()
        image = Image.new("RGBA", size=(50, 50), color=(155, 0, 0))
        image.save(file, "png")
        file.name = "test.png" + str(num)
        file.seek(0)

        return InMemoryUploadedFile(
            file, "FileField", "test.png", "image/png", sys.getsizeof(file), None
        )

    return _image_mock


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


@pytest.fixture(scope="function")
def add_expense():
    """
    Create a test expense object
    """

    def _add_expense(title, amount, category, incurred_on, created_by, file):
        expense = Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            incurred_on=incurred_on,
            created_by=created_by,
            file=file,
        )
        return expense

    return _add_expense


@pytest.fixture(scope="function")
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


@pytest.mark.django_db
def test_expense_model(create_user, image_mock):
    """
    Test creating expense model
    """
    user = create_user
    file = image_mock(1)

    expense = Expense(
        title="Chipotle",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file,
    )
    expense.save()

    assert expense.title == "Chipotle"
    assert expense.amount == "9.99"
    assert expense.category == "Dinner"
    assert expense.incurred_on == "2020-05-01"
    assert expense.updated
    assert expense.file is not None
    assert expense.created_by.id == user.id
    assert str(expense) == expense.title


@pytest.mark.django_db
def test_add_expense(client, create_user, login_user, image_mock, generate_headers):
    """
    Test adding new expense
    """
    expenses = Expense.objects.all()
    assert len(expenses) == 0

    # user = create_user
    response = login_user
    file = image_mock(1)

    access = response.data["access"]
    headers = generate_headers(access)

    resp = client.post(
        "/api/expense/",
        {
            "title": "testneww",
            "amount": "19.99",
            "category": "dinner",
            "incurred_on": "2020-05-12",
            "notes": "sdsadadsasdas",
            "file": file,
        },
        headers=headers,
    )

    assert resp.status_code == 201
    assert resp.data["title"] == "testneww"

    expenses = Expense.objects.all()
    assert len(expenses) == 1


@pytest.mark.django_db
def test_get_single_expense(
    client, create_user, login_user, image_mock, add_expense, generate_headers
):
    """
    Test get single expense by id
    """
    user = create_user
    response = login_user
    file = image_mock(1)

    access = response.data["access"]
    headers = generate_headers(access)

    expense = add_expense(
        title="Chipotle",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file,
    )

    resp = client.get(f"/api/expense/{expense.id}", headers=headers)

    assert resp.status_code == 200
    assert resp.data["title"] == "Chipotle"


@pytest.mark.django_db
def test_get_single_expense_incorrect_id(
    client, create_user, login_user, generate_headers
):
    """
    Test get single expense by incorrect id
    """
    # user = create_user
    response = login_user

    access = response.data["access"]
    headers = generate_headers(access)

    resp = client.get(f"/api/expense/noId", headers=headers)

    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_all_expenses(
    client, create_user, login_user, image_mock, add_expense, generate_headers
):
    """
    Test get all expenses by user
    """
    user = create_user
    response = login_user
    file_1 = image_mock(1)
    file_2 = image_mock(2)

    access = response.data["access"]
    headers = generate_headers(access)

    expense_one = add_expense(
        title="Chipotle",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file_1,
    )

    expense_two = add_expense(
        title="Wingstop",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file_2,
    )

    resp = client.get(f"/api/expense/", headers=headers)

    assert resp.status_code == 200
    assert resp.data[0]["title"] == expense_one.title
    assert resp.data[1]["title"] == expense_two.title


@pytest.mark.django_db
def test_delete_expense(
    client, create_user, login_user, image_mock, add_expense, generate_headers
):
    """
    Test delete expense by id
    """
    user = create_user
    response = login_user
    file = image_mock(1)

    access = response.data["access"]
    headers = generate_headers(access)

    expense = add_expense(
        title="Chipotle",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file,
    )

    resp = client.get(f"/api/expense/{expense.id}", headers=headers)

    assert resp.status_code == 200
    assert resp.data["title"] == "Chipotle"

    resp_two = client.delete(f"/api/expense/{expense.id}", headers=headers)
    assert resp_two.status_code == 204

    resp_three = client.get(f"/api/expense/", headers=headers)
    assert resp_three.status_code == 200
    assert len(resp_three.data) == 0


@pytest.mark.django_db
def test_update_expense(
    client, create_user, login_user, image_mock, add_expense, generate_headers
):
    """
    Test update expense, without updating image
    """
    user = create_user
    response = login_user
    file = image_mock(1)

    access = response.data["access"]
    headers = generate_headers(access)

    expense = add_expense(
        title="Chipotle",
        amount="9.99",
        category="Dinner",
        incurred_on="2020-05-01",
        created_by=user,
        file=file,
    )

    resp = client.put(
        f"/api/expense/{expense.id}",
        {
            "title": "Chipotle Lunch",
            "amount": "9.99",
            "category": "Lunch",
            "incurred_on": "2020-05-02",
            "notes": "Ate lunch at Chipotle",
        },
        headers=headers,
        content_type="application/json",
    )

    assert resp.status_code == 200
    assert resp.data["category"] == "Lunch"
    assert resp.data["incurred_on"] == "2020-05-02"

    resp_two = client.get(f"/api/expense/{expense.id}", headers=headers)
    assert resp_two.status_code == 200
    assert resp_two.data["category"] == "Lunch"
    assert resp_two.data["incurred_on"] == "2020-05-02"
