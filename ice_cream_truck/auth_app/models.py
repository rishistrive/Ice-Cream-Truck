from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class BaseModel(models.Model):
    """
    This model is usefull for common fields for all models.

    Attributes:
        created_at (DateTimeField): The timestamp when the instance was created.
        updated_at (DateTimeField): The timestamp when the instance was last updated.
        uuid (UUIDField): A unique identifier for the instance.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    This is a user model with additional fields and a base model with common fields.

    Attributes:
        username (CharField): A string field that stores the user's username.
        first_name (CharField): A string field that stores the user's first name.
        last_name (CharField): A string field that stores the user's last name.
        email (EmailField): An email field that stores the user's email address.
        password (CharField): A string field that stores the user's password.
        groups (ManyToManyField): A many-to-many field that associates the user with one or more user groups.
        user_permissions (ManyToManyField): A many-to-many field that associates the user with one or more permissions.
        is_staff (BooleanField): A boolean field that indicates whether the user can access the admin site.
        is_active (BooleanField): A boolean field that indicates whether the user account is active.
        date_joined (DateTimeField): A datetime field that stores the date and time the user account was created.
        is_truck_owner (BooleanField): A boolean field that indicates whether the user is a truck_owner or not.
    """
    is_truck_owner = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group', related_name='auth_app_users',
        blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='auth_app_users',
        blank=True, help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.first_name


class Truck(BaseModel):
    """
    A model that represents a truck.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Truck #{self.pk}"