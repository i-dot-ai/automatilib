INSTALLED_APPS = [
    "automatilib.core",
    "automatilib.cola",
    "django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig",
]

AUTHENTICATION_BACKENDS = [
    "automatlib.cola.backend.AuthenticationBackend",
]
