from django.conf import settings
from django.contrib.auth import get_user_model


def get_default_user():
    """
    Returns the default admin user to be used when the original creator is deleted.
    Creates the user if it doesn't exist.
    """
    User = get_user_model()

    try:
        # Try to get the superuser by username
        admin_user = User.objects.get(username=settings.DEFAULT_ADMIN_USERNAME)
    except User.DoesNotExist:
        # Create a new superuser if one doesn't exist
        admin_user = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD
        )

    return admin_user