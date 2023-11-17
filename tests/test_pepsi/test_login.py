# LOGIN_URL = "/authenticate-anyone/"
# COLA_JWK_URL = "http://127.0.0.1:8000/get-fake-cognito-user-pool-jwk/"
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login(client):
    response = client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 302

    # now we mock requests to the outside world

    response = client.get(reverse("hello-world"), follow=True)

    assert response.status_code == 200
    assert response.content.decode() == "welcome back alice@cabinetoffice.gov.uk"

    # finally we check that only the right url was mocked
    mock_get.assert_called_once_with(COLA_JWK_URL, timeout=5)

