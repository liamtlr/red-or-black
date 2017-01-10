from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User(models.Model):
    User._meta.get_field('email')._unique = True
