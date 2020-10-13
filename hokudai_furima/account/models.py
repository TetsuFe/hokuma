from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.translation import pgettext_lazy
from django.contrib.auth.validators import UnicodeUsernameValidator
from django import forms
from versatileimagefield.fields import PPOIField, VersatileImageField
from versatileimagefield.placeholder import OnDiscPlaceholderImage
import os
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, password=None,
            **extra_fields):       
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username, email=email, password=password,
            **extra_fields)
        user.is_rules_confirmed = True
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, username, password):
        if settings.DEBUG:
            user = self.create_user(username, username, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.is_rules_confirmed = True
            user.save()
            return user
        else:
            raise RuntimeError("It is not valid function in production")


class User(PermissionsMixin, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=(
            '英数字と@, ., +, -, _が使えます'),
        validators=[username_validator],
        error_messages={
            'unique': ("このユーザ名は既に登録されています"),
        },
    )
    email = models.EmailField(('email'), unique=True)
    intro = models.TextField(('intro'), max_length=200, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=False)
    icon = VersatileImageField('',upload_to='account',blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_rules_confirmed = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    objects = UserManager()

    @property
    def icon_url(self):
        if self.icon and hasattr(self.icon, 'url'):
            return self.icon.thumbnail['200x200'].url
