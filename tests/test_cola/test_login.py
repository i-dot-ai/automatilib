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

from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse
from jose import jwt

from django.test import override_settings
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


@pytest.mark.django_db
def test_already_logged_in(alice, client):
    client.force_login(alice)
    response = client.get(reverse("login"), follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_no_cookies(alice, client):
    response = client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 401


@pytest.mark.django_db
def test_cola_failure(alice, cola_client):
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        response = cola_client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "claim, value",
    [
        ("iss", "fake-issuer"),
        ("aud", "fake-audience"),
        ("exp", 0),  # 1st jan 1970
    ],
)
def test_invalid_token(client, jwt_payload, private_pem, cola_cognito_user_pool_jwk, claim, value):
    # invalidate the jwt
    jwt_payload[claim] = value
    header = {"alg": "RS256", "kid": "MY-KID-ID"}
    token = jwt.encode(jwt_payload, private_pem.decode(), algorithm="RS256", headers=header)
    client.cookies[settings.COLA_COOKIE_NAME] = token

    # now we mock requests to the outside world
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = cola_cognito_user_pool_jwk

        response = client.get(reverse("hello-world"), follow=True)

    assert response.status_code == 401


@pytest.mark.django_db
@override_settings(COLA_JWT_EXTRACTION_REGEX_PATTERN="fake-regex")
def test_invalid_regex(cola_client, cola_cognito_user_pool_jwk):
    response = cola_client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 401
