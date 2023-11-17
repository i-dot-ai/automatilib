import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def log_me_in(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = COLAUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            payload = jwt_payload(email)

            # Set a cookie with a name and value
            response = redirect(reverse(settings.LOGIN_REDIRECT_URL))
            response.set_cookie(
                settings.COLA_COOKIE_NAME,
                payload,
                max_age=3600,
            )
            return response

    form = COLAUserForm()
    return render(request, "login.html", {"form": form})


def cola_cognito_user_pool_jwk(_: HttpRequest) -> HttpResponse:
    return HttpResponse(json.dumps(COLA_COGNITO_USER_POOL_JWK, indent=2), status=200)
