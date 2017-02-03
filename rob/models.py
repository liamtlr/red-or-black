from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone


# Create your models here.
class User(models.Model):
    User._meta.get_field('email')._unique = True

class Game(models.Model):
    started_at = models.DateTimeField(
        default = timezone.now)
    ends_at = models.DateTimeField()

    def create_game(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(days=1)
        self.started_at = start_time
        self.ends_at = end_time
        self.save()
