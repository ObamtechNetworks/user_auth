from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# extend the user model by using the AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    # disable/overwrite the inbuilt django username field
    username = None

    USERNAME_FIELD = 'email'  # we want to login with an email and password
    REQUIRED_FIELDS = []