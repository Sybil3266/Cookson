from django.db import models
from django.contrib.auth.models  import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, 'register.html',  password, **extra_fields)


class User(models.Model): 
    username = models.CharField(verbose_name='아이디', unique=True, max_length=20)
    password = models.CharField(verbose_name='비밀번호', max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    is_anonymous = None
    is_authenticated = None
    def __str__(self):
        return self.username

    class Meta:
        db_table = "Cookson_user"
        verbose_name = "User"
        verbose_name_plural = "User"
