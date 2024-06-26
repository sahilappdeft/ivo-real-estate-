from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from utility.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=self.normalize_email(email),
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.role = 'superadmin'
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
        
class CustomUser(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('superadmin', 'Superadmin'),
        ('admin', 'Admin'),
        ('user', 'User')
    )
    username = None
    email = models.EmailField(unique=True)
    user_id = models.IntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES,
                            default="company", null=False, blank=False)
    last_name =models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.user_id)
