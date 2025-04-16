from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from login_history_too.models import UserLogin

User = get_user_model()


@pytest.mark.django_db()
def test_admin_login(staff, client):
    assert UserLogin.objects.count() == 0

    response = client.post(
        "/admin/login/",
        {
            "username": "testuser",
            "password": "testpass",
            "next": "/admin/",
        },
        HTTP_USER_AGENT="TestAgent/1.0",
        HTTP_X_FORWARDED_FOR="127.0.0.1",
        REMOTE_ADDR="127.0.0.1",
    )

    # Verify redirect to admin index (successful login)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == "/admin/"

    # Follow the redirect to make sure we're logged in
    admin_page = client.get("/admin/")
    assert admin_page.status_code == HTTPStatus.OK

    # Now check if login was tracked
    assert UserLogin.objects.count() == 1
    user_login = UserLogin.objects.first()
    assert user_login.user == staff
    assert user_login.ip_address == "127.0.0.1"
    # assert user_login.ip_data
    assert user_login.ua_data
