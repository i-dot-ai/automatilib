import logging
import re
from abc import abstractmethod
from urllib.parse import unquote

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from automatilib.core.i_dot_ai_utils import MethodDispatcher

LOGGER = logging.getLogger(__name__)

User = get_user_model()


def get_cola_cognito_user_pool_jwk() -> tuple[dict, str]:
    cola_issuer = f"https://cognito-idp.{settings.AWS_REGION_NAME}.amazonaws.com/{settings.COLA_COGNITO_USER_POOL_ID}"
    response = requests.get(f"{cola_issuer}/.well-known/jwks.json", timeout=5)
    assert response.status_code == 200
    cola_cognito_user_pool_jwk = response.json()
    return cola_cognito_user_pool_jwk, cola_issuer


class IAIColaLogout(MethodDispatcher):
    @abstractmethod
    def post_logout(self):
        """
        A method that is invoked post logout of a user
        """
        pass

    @abstractmethod
    def pre_logout(self):
        """
        A method that is invoked pre logout of a user
        """
        pass

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Logs a user out of the system and removes the COLA JWT from their browser cookies
        :param request: The HTTP request
        :return: A HTTP response without the JWT token cookie
        """
        logout(request)
        redirect_url = settings.LOGIN_URL
        response = redirect(reverse(redirect_url or "index"))
        response.delete_cookie(settings.COLA_COOKIE_NAME)
        return response


class IAIColaLogin(MethodDispatcher):
    @abstractmethod
    def pre_login(self):
        """
        A method that is invoked after checking if a user is already logged in,
        but before performing any actions on the request
        """
        pass

    @abstractmethod
    def post_login(self):
        """
        A method that is invoked after `handle_claims` and logging/authenticating a user,
        but before returning an HTTP response
        """
        pass

    @abstractmethod
    def handle_user_jwt_details(self, user: User, token_payload: dict) -> None:
        """
        A method that is invoked after logging/authenticating a user and before `post_login`,
        but before returning an HTTP response.
        Email is already taken from the token and saved to the user object before this
        :param user: The user that is logged in and authenticated
        :param token_payload: The token payload that includes information from COLA
        """
        pass

    def get(self, request: HttpRequest) -> HttpResponse:
        redirect_url = settings.LOGIN_REDIRECT_URL
        if request.user.id:
            return redirect(reverse(redirect_url or "index"))

        self.pre_login()

        if not (cola_cookie := request.COOKIES.get(settings.COLA_COOKIE_NAME, None)):
            LOGGER.error("No cookie found")
            return HttpResponseServerError()
        if not (
            regex_match := re.search(
                settings.COLA_JWT_EXTRACTION_REGEX_PATTERN,
                unquote(cola_cookie),
            )
        ):
            LOGGER.error("No cookie regex match found")
            return HttpResponseServerError()

        cola_cognito_user_pool_jwk, cola_issuer = get_cola_cognito_user_pool_jwk()
        header = jwt.get_unverified_header(regex_match.group(0))
        jwt_kid = header["kid"]
        public_key = next(key for key in cola_cognito_user_pool_jwk["keys"] if key["kid"] == jwt_kid)

        try:
            token = regex_match.group(0)
            token = ".".join(token.split(".")[:3])
            payload = jwt.decode(
                token=token,
                audience=settings.COLA_COGNITO_CLIENT_ID,
                issuer=cola_issuer,
                algorithms=["RS256"],
                key=public_key,
                options={
                    "require_aud": True,
                    "require_iat": True,
                    "require_exp": True,
                    "require_iss": True,
                    "require_sub": True,
                },
            )

        except (ExpiredSignatureError, JWTClaimsError, JWTError, KeyError) as error:
            LOGGER.error("cookie error:", type(error).__name__)
            return HttpResponseServerError()

        authenticated_user = {
            "email": payload["email"],
        }

        if user := authenticate(request=request, user_response=authenticated_user):
            LOGGER.info("Attempting to log user in")
            LOGGER.debug(user.__dict__)
            user = authenticate(request=request, user_response=authenticated_user)
            user.save()
            self.handle_user_jwt_details(user, payload)
            login(request, user)
            self.post_login()
            return redirect(reverse(redirect_url or "index"))

        LOGGER.error("No user found")
        return HttpResponseServerError()
