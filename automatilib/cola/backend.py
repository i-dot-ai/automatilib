import logging
from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

LOGGER = logging.getLogger(__name__)

UserModel = get_user_model()


class COLAAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        """
        Get user response given by JWT token from kwargs and update the user based on this
        :param request: The HTTP request that is requesting authentication
        :param username: The users username (not used)
        :param password: The users password (not used)
        :param kwargs: The kwargs dict containing the JWT token body
        :return: The user object
        """
        try:
            email = kwargs["user_response"]["email"]
        except KeyError:
            LOGGER.error("non-COLA authentication attempt made")
            return None
        user, created = UserModel.objects.get_or_create(
            email=email,
        )
        if created:
            LOGGER.info(f"created new user: {email} from COLA authentication")
        return user

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
