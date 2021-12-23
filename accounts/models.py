from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):    
    use_in_migrations = True
    
    def _create_user(self, username, email, password=None, **extra_fields):
        values = [username, email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, default='avatars/default.jpg')   
    date_of_birth = models.DateField(blank=True, null=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    read_message_last_time = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return '<User {}>'.format(self.username)

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.id)])

    def new_messages(self):
        last_read_time = self.read_message_last_time or datetime(1967, 6, 6)
        return Message.objects.filter(recipient=self).filter(
            Message.timestamp > last_read_time).count()


class Message(models.Model):
    sender = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name="recipient")
    body = models.TextField(max_length=450)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<Message: {}>'.format(self.body)