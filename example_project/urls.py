from django.urls import path

import cola
from example_project import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello-world"),
    path("login/", views.fake_login, name="login"),
    path("post-login/", cola.ColaLogin.as_view(), name="post-login"),
    path("logout/", cola.ColaLogout.as_view(), name="logout"),
]
