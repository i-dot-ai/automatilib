import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from automatilib.cola.views import COLA_ISSUER
from automatilib.pepsi.core import FakeTokenFactory
from automatilib.pepsi.forms import COLAUserForm

FAKE_TOKEN_FACTORY = FakeTokenFactory(COLA_ISSUER, settings.COLA_COGNITO_CLIENT_ID)


def authenticate_anyone(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = COLAUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            payload = FAKE_TOKEN_FACTORY.generate_token(email)

            # Set a cookie with a name and value
            response = redirect("/post-login/")
            response.set_cookie(
                settings.COLA_COOKIE_NAME,
                payload,
                max_age=3600,
            )
            return response

    form = COLAUserForm()
    return render(request, "login.html", {"form": form})


def get_fake_cognito_user_pool_jwk(_: HttpRequest) -> HttpResponse:
    cola_cognito_user_pool_jwk = FAKE_TOKEN_FACTORY.cola_cognito_user_pool_jwk()
    return HttpResponse(json.dumps(cola_cognito_user_pool_jwk), status=200, content_type="application/json")