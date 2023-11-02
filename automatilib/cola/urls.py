from django.urls import path

from automatilib.cola import views

url_patterns = [
    path("post-login/", views.ColaLogin.as_view(), name="post-login"),
    path("logout/", views.ColaLogout.as_view(), name="logout"),
]
