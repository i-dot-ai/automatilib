INSTALLED_APPS = [
    "automatilib.cola_auth",
]

AUTHENTICATION_BACKENDS = [
    "automatilib.cola_auth.backend.AuthenticationBackend",
]
