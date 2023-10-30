# i.AI Shared Code


Free software: MIT license


## Features

* Choices utility
* Timestamped, UUID and base user models
* Initial migration for above models
* Logic for authenticating with COLA


## Settings

* `LOGIN_REDIRECT_URL` - The URL to redirect users to post-login
* `LOGIN_URL` - The URL to redirect users to if they are not logged in
* `COLA_COOKIE_NAME` - The name of the cookie to check for COLA JWT
* `COLA_JWT_EXTRACTION_REGEX_PATTERN` - The regex used to extract the JWT from the COLA cookie
* `COLA_COGNITO_CLIENT_ID` - The cognito client ID found in AWS
* `AWS_REGION_NAME` - The AWS region that the user pool and cognito client live in
* `COLA_COGNITO_USER_POOL_ID` - The cognito user pool ID in AWS

This is where some of the above can be found:

* `COLA_COOKIE_NAME`: In your json settings file for COLA
* `COLA_COOKIE_DOMAIN`: `cabinetoffice.gov.uk`
* `COLA_COGNITO_CLIENT_ID`: In AWS, go to your cognito user pool, then to app integration, then at the bottom you can find your client ID in the table
* `AWS_REGION_NAME`: Whichever region in AWS your Cognito pool lives, likely to be `eu-west-2`
* `COLA_COGNITO_USER_POOL_ID`: In AWS, go to your cognito user pool, in the top table called `User pool overview`, your `User pool ID` is there
* `COLA_LOGIN_URL`: Ask the COLA team for this URL
* `COLA_JWT_REGEX_PATTERN`: This is one you can adjust how you want to, the baseline is `(?<=:).*(?=\.)`


## To make use of COLA

see the [example settings](example_project/settings.py) in this repo

Add these into your `INSTALLED_APPS` settings:

```python
INSTALLED_APPS = [
    "core.apps.IdotAIConfig",
    "cola.apps.ColaAuthConfig",
    ...
]
```

Add this into your `AUTHENTICATION_BACKEND` setting:

```python
AUTHENTICATION_BACKENDS = [
    "cola.backend.COLAAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",  # This includes the default backend
]
```

Import and add the following to your url_patterns:
```python
from automatilib.cola.cola_urls import url_patterns as cola_urls
urlpatterns = other_urlpatterns + cola_urls
```


## How to run Tests

```commandline
DJANGO_SETTINGS_MODULE=example_project.settings pytest --cov cola --cov core --cov-report term-missing --cov-fail-under 80
```
