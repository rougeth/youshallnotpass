from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, null=True,
                              blank=True)
    username = models.CharField(max_length=250, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    github_synced_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    def get_short_name(self):
        return self.get_username()

    def get_full_name(self):
        return self.get_username()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def github_social_user(self):
        for social_user in self.social_auth.all():
            if social_user.provider == 'github':
                return social_user

    @property
    def github_headers(self):
        return {
            'Authorization': 'token ' + self.github_social_user.access_token,
            'Accept': 'application/vnd.github.v3+json'
        }
