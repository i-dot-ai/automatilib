from base64 import urlsafe_b64encode
from datetime import datetime, timedelta

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwt


from django.http import HttpRequest, HttpResponse

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

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
cola_cognito_user_pool_jwk = {"keys": [payload]}

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)


def login(request: HttpRequest) ->HttpResponse:

