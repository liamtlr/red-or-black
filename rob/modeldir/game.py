from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from rob.modeldir.player import *
# from rob.modeldir.selection import *
from django.contrib.postgres.fields import ArrayField
import random
# from django.db.models import Queryset

class GameQuerySet(models.QuerySet):

    def get_expired_games(self):
        return self.filter(ends_at__lte=datetime.now(), in_progress=True).distinct()

    def get_first_round_games(self, user_id):
        return self.filter(round_no=1,
                           ends_at__gte=datetime.now()).exclude(selection__player_id=user_id).distinct()

    def get_pending_games(self, user_id):
        return self.filter(ends_at__gte=datetime.now(), selection__player_id=user_id, selection__active=True).exclude(selection__colour="").distinct()

    def get_lost_games(self, user_id):
        return self.filter(selection__player_id=user_id, selection__active=False, selection__viewable=True).distinct()

    def get_won_games(self, user_id):
        return self.filter(in_progress=False, selection__player_id=user_id, selection__active=True, selection__viewable=True).distinct()

    def get_live_games(self, user_id):
        return self.filter(in_progress=True, selection__player_id=user_id, selection__active=True, selection__colour="").distinct()


class GameManager(models.Manager):

    def get_queryset(self):
        return GameQuerySet(self.model, using=self._db)

    def get_expired_games(self):
        return self.get_queryset().get_expired_games()

    def get_first_round_games(self, user_id):
        return self.get_queryset().get_first_round_games(user_id)

    def get_pending_games(self, user_id):
        return self.get_queryset().get_pending_games(user_id)

    def get_lost_games(self, user_id):
        return self.get_queryset().get_lost_games(user_id)

    def get_won_games(self, user_id):
        return self.get_queryset().get_won_games(user_id)

    def get_live_games(self, user_id):
        return self.get_queryset().get_live_games(user_id)



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

    objects = GameManager()


    def create_game(self, user):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=1)
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

    def select_colour(self):
        choices = ["red", "black"]
        self.colour = random.choice(choices)
        self.previous_colours.append(self.colour)
        self.save()

    def increment_round(self):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=5)
        self.round_no += 1
        self.started_at = start_time
        self.ends_at = end_time
        self.save()

    def end_game(self):
        self.in_progress = False
        self.save()

    def get_game_data(self):
        losers_by_round = []
        counter = 1
        previous_colours = self.previous_colours
        previous_colours.pop(0)
        while counter <= self.round_no:
            this_round_losers = self.selection_set.filter(active=False, lost_round=counter).count()
            losers_by_round.append(this_round_losers)
            counter+=1
        return zip(previous_colours, losers_by_round)

    def hide_game(self):
        self.viewable = False
        self.save()
