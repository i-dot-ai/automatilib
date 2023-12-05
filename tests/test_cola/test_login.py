from unittest.mock import patch

import pytest
from django.urls import reverse
from jose import jwt

from automatilib.cola.views import COLA_JWK_URL


@pytest.mark.django_db
def test_login(alice, cola_client, cola_cognito_user_pool_jwk):
    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 302

    # check alice is not an admin user
    assert not alice.is_staff

    # now we mock requests to the outside world
    with patch("requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = cola_cognito_user_pool_jwk

        response = cola_client.get(reverse("hello-world"), follow=True)

    assert response.status_code == 200
    assert response.content.decode() == "welcome back alice@cabinetoffice.gov.uk"

    alice.refresh_from_db()
    # now check that alice is an admin user
    assert alice.is_staff

    # finally we check that only the right url was mocked
    mock_get.assert_called_once_with(COLA_JWK_URL, timeout=5)


@pytest.mark.django_db
def test_logout(alice, cola_client, settings):
    cola_client.force_login(alice)
    assert alice.is_authenticated

    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 200

    response = cola_client.get(reverse("logout"))

    # check that cookie has been flushed
    assert not cola_client.cookies[settings.COLA_COOKIE_NAME].value

    assert not cola_client.session.get('_auth_user_id')  # alice logged out

    assert response.status_code == 302


@pytest.mark.django_db
def test_already_logged_in(alice, client):
    client.force_login(alice)
    response = client.get(reverse("post-login"), follow=True)
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
@pytest.mark.parametrize("cola_login_failure_url", [None, "login-failure"])
def test_invalid_token(
    settings, client, jwt_payload, private_pem, cola_cognito_user_pool_jwk, claim, value, cola_login_failure_url
):
    settings.COLA_LOGIN_FAILURE = cola_login_failure_url
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

    # check that invalid cookie has been flushed
    assert not client.cookies[settings.COLA_COOKIE_NAME].value
    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticate_fails(cola_client, cola_cognito_user_pool_jwk):
    """same as test_login but this time we force the authenticate method to fail"""
    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 302

    # now we mock requests to the outside world
    with patch("requests.get") as mock_get, patch("automatilib.cola.views.authenticate") as mock_authenticator:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = cola_cognito_user_pool_jwk

        mock_authenticator.return_value = None

        response = cola_client.get(reverse("hello-world"), follow=True)

    assert response.status_code == 401
    assert response.content.decode() == "Unauthorized"

    # finally we check that only the right url was mocked
    mock_get.assert_called_once_with(COLA_JWK_URL, timeout=5)
