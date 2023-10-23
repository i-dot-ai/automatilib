from django.urls import path
from i_dot_ai_cola_views import IAIColaLogin, IAIColaLogout

app_name = "cola_auth"
url_patterns = [
    path("post-login/", IAIColaLogin.as_view(), name="post-login"),
    path("logout/", IAIColaLogout.as_view(), name="logout"),
]
