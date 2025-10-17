from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def _create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password() 
        user.save()
        return user

    def create_user(self, email, password=None, *args, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_active", True)
        return self._create_user(email, password, *args, **kwargs)

    def create_superuser(self, email, password=None, *args, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be a staff")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be a superuser")
        return self._create_user(email, password, *args, **kwargs)
    

class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(_("staff_status"), default=False)
    is_active = models.BooleanField(_("active_status"), default=True)
    is_superuser = models.BooleanField(_("superuser_status"), default=False)
    email = models.EmailField(_("email_address"), unique=True, null=True)
    username = models.CharField(max_length=100, unique=True, db_index=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)

    is_email_verified = models.BooleanField(
        _("email verification status"), default=False
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.name}-{self.username}"

    def set_full_name(self, name):
        parts = name.split(" ")
        if len(parts) < 1:
            return
        self.first_name = parts[0] if parts[0] else None
        last_name = " ".join(parts[1:])
        self.last_name = last_name if last_name.strip() else None

    def get_full_name(self):
        return self._get_full_name(self.first_name, self.last_name)

    name = property(get_full_name, set_full_name)

    @staticmethod
    def _get_full_name(first_name, last_name):
        full_name = ""
        if first_name:
            full_name += first_name + " "
        if last_name:
            full_name += last_name
        return full_name.strip() or None