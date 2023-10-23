INSTALLED_APPS = [
    "automatilib.automatilib.core",
    "automatilib.automatilib.cola_auth",
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
]

AUTHENTICATION_BACKENDS = [
    "automatilib.automatilib.cola_auth.backend.AuthenticationBackend",
]

AUTH_USER_MODEL = "automatilib.core.User"
