from base64 import urlsafe_b64encode
from datetime import datetime, timedelta

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.conf import settings
from django.contrib.auth.models import User
from jose import jwt

from cola.views import COLA_ISSUER


@pytest.fixture
def alice():
    user = User.objects.create_user(username="alice", email="alice@cabinetoffice.gov.uk")
    yield user


@pytest.fixture()
def private_key():
    # Generate an RSA key pair for signing
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    yield key


@pytest.fixture
def cola_cognito_user_pool_jwk(private_key):
    public_key = private_key.public_key()
    public_numbers = public_key.public_numbers()
    e, n = public_numbers.e, public_numbers.n

    def url_encode_public_numbers(number):
        # Serialize "e" (public exponent) and "n" (modulus) to bytes
        number_as_bytes = number.to_bytes((number.bit_length() + 7) // 8, "big")
        return urlsafe_b64encode(number_as_bytes).decode("utf-8")

    # Encode "e" and "n" as base64 URL-safe strings
    e_base64 = url_encode_public_numbers(e)
    n_base64 = url_encode_public_numbers(n)

    # Create a JSON payload
    payload = {"alg": "RS256", "e": e_base64, "kid": "MY-KID-ID", "kty": "RSA", "n": n_base64, "use": "sig"}
    yield {"keys": [payload]}


@pytest.fixture()
def token(alice, private_key):
    payload = {
        "sub": "2612f274-f081-70fc-e3f3-7da285b561a4",
        "email_verified": True,
        "custom:lastLogin": "2023-10-06T11:06:13.730Z",
        "custom:features": "test",
        "iss": COLA_ISSUER,
        "cognito:username": alice.username,
        "given_name": alice.username,
        "aud": settings.COLA_COGNITO_CLIENT_ID,
        "event_id": "09102e2f-f60f-480f-99e0-09b4ea451568",
        "token_use": "id",
        "custom:phoneNumber": "+07700900676",
        "auth_time": 1696591062,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": 1696591062,
        "family_name": "Smith",
        "email": alice.email,
        "custom:isAdmin": "true",
    }

    header = {"alg": "RS256", "kid": "MY-KID-ID"}

    # Serialize the private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    token = jwt.encode(payload, private_pem.decode(), algorithm="RS256", headers=header)
    yield token


@pytest.fixture
def cola_client(client, token):
    client.cookies[settings.COLA_COOKIE_NAME] = token
    yield client
