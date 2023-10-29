import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login(cola_client, cola_cognito_user_pool_jwk, mocker):
    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 302

    mocker.patch("cola.views.get_cola_cognito_user_pool_jwk", return_value=cola_cognito_user_pool_jwk)

    response = cola_client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 200
    assert response.content.decode() == "welcome back alice@cabinetoffice.gov.uk"


@pytest.mark.django_db
def test_logout(alice, cola_client):
    cola_client.force_login(alice)
    assert alice.is_authenticated

    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 200

    response = cola_client.get(reverse("logout"))
    # assert not alice.is_authenticated
    assert response.status_code == 302
