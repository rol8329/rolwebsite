from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fix the conflicts by adding related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_set",  # Changed to avoid conflict
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",  # Changed to avoid conflict
        related_query_name="custom_user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'account_user'  # Use different table name

    def __str__(self):
        return self.email

    @property
    def role(self):
        """Get user's primary role based on groups"""
        if self.groups.filter(name='owner').exists():
            return 'owner'
        elif self.groups.filter(name='creator').exists():
            return 'creator'
        elif self.groups.filter(name='reader').exists():
            return 'reader'
        return 'reader'  # Default role

    @property
    def permissions_level(self):
        """Get numerical permission level"""
        role_levels = {
            'reader': 1,
            'creator': 2,
            'owner': 3
        }
        return role_levels.get(self.role, 1)