import pytest
from django.test import override_settings
from django.urls import reverse


@pytest.mark.django_db
@override_settings(LOGIN_URL="/authenticate-anyone/")
def test_login(client, mocker):
    initial_response = client.get(reverse("hello-world"))
    assert initial_response.status_code == 302
    assert initial_response.url == "/authenticate-anyone/?next=/hello/"

    email = "alice@cabinetoffice.gov.uk"
    mocker.patch(
        "automatilib.cola.views.get_request", return_value=client.get(reverse("get_fake_cognito_user_pool_jwk"))
    )
    login_response = client.post(initial_response.url, data={"email": email}, follow=True)

    assert login_response.status_code == 200
    assert login_response.content.decode() == f"welcome back {email}"
