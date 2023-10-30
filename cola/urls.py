from django.urls import path

from cola import views

url_patterns = [
    path("login/", views.ColaLogin.as_view(), name="login"),
    path("logout/", views.ColaLogout.as_view(), name="logout"),
]
