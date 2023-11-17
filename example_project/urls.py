from django.urls import path

from automatilib.cola.urls import url_patterns as cola_urls
from automatilib.pepsi.urls import url_patterns as pepsi_urls
from example_project import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello-world"),
    path("my_account/", views.my_account, name="my-account"),
] + cola_urls + pepsi_urls
