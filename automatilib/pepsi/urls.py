from django.urls import path

from automatilib.pepsi import views

url_patterns = [
    path("authenticate-anyone/", views.authenticate_anyone, name="authenticate_anyone"),
    path("get-fake-cognito-user-pool-jwk/", views.get_fake_cognito_user_pool_jwk, name="get_fake_cognito_user_pool_jwk")
]
