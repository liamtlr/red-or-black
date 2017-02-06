from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from rob.modeldir.player import *
from django.contrib.postgres.fields import ArrayField


class Game(models.Model):
    started_at = models.DateTimeField(
        default = timezone.now)
    ends_at = models.DateTimeField()
    round_no = models.IntegerField(default=1)
    owner = models.ForeignKey(Player,blank=True, null=True, default="", on_delete=models.CASCADE)
    members = models.ManyToManyField(Player, through='Selection')
    colour = models.CharField(max_length=10, default='', blank=True)
    previous_colours = ArrayField(models.CharField(max_length=100, null=True, blank=True, default=["placeholder"]), null=True, blank=True, default=["placeholder"])
    in_progress = models.BooleanField(default=True, blank=True)
    pot = models.IntegerField(default=0, blank=True)


    def create_game(self, user):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=2)
        self.started_at = start_time
        self.ends_at = end_time
        self.owner = user
        self.save()

    def return_end_time(self):
        time = self.ends_at
        join = ", "
        first_bit = time.strftime('%Y')
        middle_bit = str(time.month - 1)
        end_bit = time.strftime('%d, %H, %M, %S')
        return first_bit + join + middle_bit + join + end_bit

    def next_round(self):
        choices = ["red", "black"]
        self.colour = random.choice(choices)
        self.round_no += 1
        self.save()
