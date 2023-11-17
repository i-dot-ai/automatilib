from base64 import urlsafe_b64encode
from datetime import datetime, timedelta

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwt


def url_encode_public_numbers(number):
    """Serialize "e" (public exponent) and "n" (modulus) to bytes"""
    number_as_bytes = number.to_bytes((number.bit_length() + 7) // 8, "big")
    return urlsafe_b64encode(number_as_bytes).decode("utf-8")


class FakeTokenFactory:
    def __init__(self, iss, aud):
        self.iss = iss
        self.aud = aud

        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def cola_cognito_user_pool_jwk(self) -> dict:
        # Create a JSON payload
        public_key = self.private_key.public_key()
        public_numbers = public_key.public_numbers()
        e, n = public_numbers.e, public_numbers.n

        # Encode "e" and "n" as base64 URL-safe strings
        e_base64 = url_encode_public_numbers(e)
        n_base64 = url_encode_public_numbers(n)

        payload = {"alg": "RS256", "e": e_base64, "kid": "MY-KID-ID", "kty": "RSA", "n": n_base64, "use": "sig"}
        return {"keys": [payload]}

    def generate_token(self, email: str, **kwargs: str) -> str:
        payload = {
            "sub": "2612f274-f081-70fc-e3f3-7da285b561a4",
            "email_verified": True,
            "custom:lastLogin": "2023-10-06T11:06:13.730Z",
            "custom:features": "test",
            "iss": self.iss,
            "aud": self.aud,
            "event_id": "09102e2f-f60f-480f-99e0-09b4ea451568",
            "token_use": "id",
            "custom:phoneNumber": "+07700900676",
            "auth_time": 1696591062,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": 1696591062,
            "email": email,
        }

        payload.update(kwargs)

        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        token = jwt.encode(
            payload,
            pem.decode(),
            algorithm="RS256",
            headers={"alg": "RS256", "kid": "MY-KID-ID"},
        )
        return token
