from unittest.mock import patch

import pytest
from django.test import override_settings
from django.urls import reverse

from automatilib.pepsi.views import FAKE_TOKEN_FACTORY


@pytest.mark.django_db
@override_settings(LOGIN_URL="/authenticate-anyone/")
def test_login(client):
    initial_response = client.get(reverse("hello-world"))
    assert initial_response.status_code == 302
    assert initial_response.url == "/authenticate-anyone/?next=/hello/"

    email = "alice@cabinetoffice.gov.uk"
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = FAKE_TOKEN_FACTORY.cola_cognito_user_pool_jwk()

        login_response = client.post(initial_response.url, data={"email": email}, follow=True)

    assert login_response.status_code == 200
    assert login_response.content.decode() == f"welcome back {email}"
