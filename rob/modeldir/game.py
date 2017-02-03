from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from rob.modeldir.player import *

class Game(models.Model):
    started_at = models.DateTimeField(
        default = timezone.now)
    ends_at = models.DateTimeField()
    members = models.ManyToManyField(Player, through='Selection')

    def create_game(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(days=1)
        self.started_at = start_time
        self.ends_at = end_time
        self.save()

    def return_end_time(self):
        time = self.ends_at
        join = ", "
        first_bit = time.strftime('%Y')
        middle_bit = str(time.month - 1)
        end_bit = time.strftime('%d, %H, %M, %S')
        return first_bit + join + middle_bit + join + end_bit
