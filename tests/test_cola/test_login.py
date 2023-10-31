from unittest.mock import patch

import pytest
from django.urls import reverse

from automatilib.cola.views import COLA_URL


@pytest.mark.django_db
def test_login(cola_client, cola_cognito_user_pool_jwk):
    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 302

    # now we mock requests to the outside world
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = cola_cognito_user_pool_jwk

        response = cola_client.get(reverse("hello-world"), follow=True)

    assert response.status_code == 200
    assert response.content.decode() == "welcome back alice@cabinetoffice.gov.uk"

    # finally we check that only the right url was mocked
    mock_get.assert_called_once_with(COLA_URL, timeout=5)


@pytest.mark.django_db
def test_logout(alice, cola_client):
    cola_client.force_login(alice)
    assert alice.is_authenticated

    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 200

    response = cola_client.get(reverse("logout"))
    # assert not alice.is_authenticated
    assert response.status_code == 302
