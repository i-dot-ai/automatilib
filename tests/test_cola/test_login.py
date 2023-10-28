import pytest
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

cola_cognito_user_pool_jwk = {
    "keys": [
        {
            "alg": "RS256",
            "e": "AQAB",
            "kid": "q/tO4RmaRXZ+/n77riA8oIwsLBQbqpSVeKXod4YM+P0=",
            "kty": "RSA",
            "n": "1VZNZnN29wLj4SrqEMgusex5NZUZ4Xehd2L7ioelaNfN-xmZd-F62bqSAa-wi-Y4FOErD9RJ7PzPfXDzMfvkOuFAUbMFhoFVa2LuuMez9_m9JmrGJBVI8TwhQuy089ha73R8Z5QHhah7YQQgrJHHiPQhGhDj8KYV8Lo8RFtE_lHwthCsL5u0xjaGxwOuTeL0zY5mjid3D3cPWqiHhB60nLe4lE9q3V3-w19kY64TuwM6zp6OyIgb8FNM7-0tF1KMY0_1zLPBpyqMmtdh851xQEj_VqyWpiSXO45oW6Ls76pfaS85g29Tcyjlp2_5SkewjS5JTNWWBTx_AojzEZ49fQ",
            "use": "sig",
        },
        {
            "alg": "RS256",
            "e": "AQAB",
            "kid": "zvy8JuQhTptUGlUYJQhQate1HEiKwuTA8OSy4LamYEU=",
            "kty": "RSA",
            "n": "03uqE0sDiwI3D_Cccos7z2YvrfBoHNlV5c4NxIVfJ9fBj0J2riu9ziPjD5Q8UbO_dvlFRYAKRq6-klVvu7eo5ze1iMK53PMA7vgM9snU7I01pVONGdEGOQpXgLeRMvCWhS161ls9ULs5QkRNQ6ocl8YNUPnpYL0aqBf-8DIlVW_grpYJkMdbgl79M1pJDQLFjoFIKA8nS636szm9xpqH809oi7pq61t2NTfI_LoWd6_czMjn4XBXDEbLBAWOdrR1k6k8kOrqszIqM7xCySKElXFh5MD1IBgaBS0GU4z3PH-CFuLjem0HUoi64NAZudx7rlOt1hXxafvVreRTR2GNLQ",
            "use": "sig",
        },
    ]
}
cola_issuer = "https://cognito-idp.eu-west-2.amazonaws.com/eu-west-****"


@pytest.fixture
def alice():
    user = User.objects.create_user(username="alice@cabinetoffice.gov.uk")
    yield user


@override_settings(
    JWT_DECODE_OPTIONS={
        "verify_aud": False,
        "verify_iss": False,
        "verify_exp": False,
    }
)
@pytest.mark.django_db
def test_login(alice, cola_client, mocker):
    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 302

    mocker.patch("cola.views.get_cola_cognito_user_pool_jwk", return_value=(cola_cognito_user_pool_jwk, cola_issuer))

    response = cola_client.get(reverse("hello-world"), follow=True)
    assert response.status_code == 200
    assert response.content.decode() == "you are logged in"


@pytest.mark.django_db
def test_logout(alice, cola_client):
    cola_client.force_login(alice)
    assert alice.is_authenticated

    response = cola_client.get(reverse("hello-world"))
    assert response.status_code == 200

    response = cola_client.get(reverse("logout"))
    # assert not alice.is_authenticated
    assert response.status_code == 302
