import pytest
from django.http import HttpRequest
from jose import jwt

from automatilib.cola.backend import COLAAuthenticationBackend


@pytest.fixture
def backend():
    yield COLAAuthenticationBackend()


@pytest.mark.django_db
def test_authenticate(backend):
    email = "someone@cabinetoffice.gov.uk"
    user = backend.authenticate(request=HttpRequest(), user_response={"email": email})
    assert user.email == email


def test_authenticate_fail(backend):
    assert not backend.authenticate(request=HttpRequest())


@pytest.mark.django_db
def test_get_user(backend, alice):
    assert backend.get_user(alice.pk) == alice


@pytest.mark.django_db
def test_get_user_fails(backend):
    assert not backend.get_user(123)


def test_get():
    token = "s:eyJraWQiOiJJYnJkcmVMcDNSVHZydytXT1pFaEh6TjhVeGZkU3pJYnh6bmh1TkJGWFRvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI5ODA2ZDEwZC03YzAwLTRmZTEtOWE3MC1kZjExZTkyMmIwYTAiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiY3VzdG9tOmxhc3RMb2dpbiI6IjIwMjMtMTEtMjhUMTc6MjM6MTkuODY0WiIsImN1c3RvbTpmZWF0dXJlcyI6InRlc3QiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0yLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMl9HQjlEdnhoTHAiLCJjb2duaXRvOnVzZXJuYW1lIjoiZ2VvcmdlLmJ1cnRvbkBjYWJpbmV0b2ZmaWNlLmdvdi51ayIsImdpdmVuX25hbWUiOiJnZW9yZ2UiLCJvcmlnaW5fanRpIjoiNWFhODFhN2EtZWRiMy00NzQzLThhNTYtMjdjOWY4NGZhYTMwIiwiYXVkIjoiNm9paTRzYjBja2xzdDhrcjVyNWtoaGMydmciLCJldmVudF9pZCI6IjYwMjBlNmUyLWVjNTItNDRjMy1iMjg0LTRkYTBkOWI5MjVhYiIsInRva2VuX3VzZSI6ImlkIiwiY3VzdG9tOnBob25lTnVtYmVyIjoiMDc5NTE2Njc4NTIiLCJhdXRoX3RpbWUiOjE3MDExOTM2NTMsImV4cCI6MTcwMTE5Mzk1MywiaWF0IjoxNzAxMTkzNjUzLCJmYW1pbHlfbmFtZSI6ImJ1cnRvbiIsImp0aSI6IjA1NGE4MmZiLTMxNjgtNDcxZS05MzQ2LTg2YTlmMTI0ZTBmMCIsImVtYWlsIjoiZ2VvcmdlLmJ1cnRvbkBjYWJpbmV0b2ZmaWNlLmdvdi51ayIsImN1c3RvbTppc0FkbWluIjoidHJ1ZSJ9.S6BcCsi92-Wa0EpUnZ3a9wADQsOzEw2ZgGHF6YD9NqJTS9twjeXIAQqgBJE_2iHars87eucJIIvUpMSyedDtDBA08zmplcRJxheQzkbLSQbc3Bz3I0NyZEBB7cJyLLXKRNth8zU_KN2HtLeDldzWUIYxaB_9gW6wJ2XdTknhktWvSZk_a4bM4qUzj4_Ms7-dzy--485Xnmnwfa3LZsXm2PcbE3ciRhbvHB2RNWMCpep5uq_uHdwP5aiT332szUJ7liMSsSvGI3aCcWqhj6cmlw3X99mKCloXQj0jg4Bd4JZBJGpm8iHkYXTo61CqwS3ZmngC_eF2CkxHzGyVSAx-_g.KT9O7rXjtraAd4AVxdeSXh6ljQ5og9L+soZ02Tagh0A"
    if token.startswith("s:") and token.count(".") == 3:
        token = ".".join(token[2:].split(".")[:3])

    header = jwt.get_unverified_header(token)
