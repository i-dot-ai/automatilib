from django.urls import path
from i_dot_ai_cola_views import IAIColaLogin, IAIColaLogout

app_name = "cola_auth"
urlpatterns = [
    path("post-login/", IAIColaLogin, name="post-login"),
    path("logout/", IAIColaLogout, name="logout"),
]
