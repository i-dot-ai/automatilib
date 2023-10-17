INSTALLED_APPS = [
    "automatilib.automatilib.cola_auth",
]

AUTHENTICATION_BACKENDS = [
    "automatilib.automatilib.cola_auth.backend.AuthenticationBackend",
]
