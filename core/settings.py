INSTALLED_APPS = [
    "automatilib.automatilib.core",
    "automatilib.automatilib.cola",
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
]

AUTHENTICATION_BACKENDS = [
    "automatlib.cola.backend.AuthenticationBackend",
]

AUTH_USER_MODEL = "automatilib.core.User"
