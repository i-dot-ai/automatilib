import pytest
from django.http import HttpRequest

from automatilib.cola.backend import COLAAuthenticationBackend


@pytest.fixture
def backend():
    yield COLAAuthenticationBackend()


@pytest.mark.django_db
def test_authenticate(backend):
    email = "Someone@cabinetoffice.gov.uk"
    user = backend.authenticate(request=HttpRequest(), user_response={"email": email})
    assert user.email == email.lower()


def test_authenticate_fail(backend):
    assert not backend.authenticate(request=HttpRequest())


@pytest.mark.django_db
def test_get_user(backend, alice):
    assert backend.get_user(alice.pk) == alice


@pytest.mark.django_db
def test_get_user_fails(backend):
    assert not backend.get_user(123)
