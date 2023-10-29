from django.urls import path

import cola
from example_project import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello-world"),
    path("my_account/", views.my_account, name="my-account"),
    path("login/", cola.ColaLogin.as_view(), name="login"),
    path("logout/", cola.ColaLogout.as_view(), name="logout"),
]
