from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


# This is my custom user class. Not Django's. Because they're suck.
# If you wanna create Profile, for example, make another app. Don't do it here because
# this is custom user model so it lacks stuff.


class UserManager(BaseUserManager):
    # User creator
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)  # also how I change the password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    # Staff User creator
    def create_staff_user(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user

    # SuperUser creator
    def create_super_user(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)  # username equivalent
    # full_name = models.CharField(max_length=225, blank=True, null=True)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user. non-superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm = models.BooleanField(default=False)
    # Confirm_date = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username equivalent
    # USERNAME_FIELD and password is required by default
    REQUIRED_FIELDS = []  # ['full_name'] # also apply to python manage.py createsuperuser

    objects = UserManager()

    # Because we're only use emails for legit users
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


# Email for guest users
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
