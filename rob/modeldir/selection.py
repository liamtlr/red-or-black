from django.db import models
from rob.modeldir.player import *
from rob.modeldir.game import *

class SelectionQuerySet(models.QuerySet):
    def get_winners(self, game_id, colour):
        return self.filter(game_id=game_id).filter(active=True).filter(colour=colour)

    def get_losers(self, game_id, colour):
        return self.filter(game_id=game_id).filter(active=True).exclude(colour=colour)

    def get_reds(self, game_id):
        return self.filter(active=True, game_id=game_id, colour="red")

    def get_blacks(self, game_id):
        return self.filter(active=True, game_id=game_id, colour="black")

class SelectionManager(models.Manager):
    def get_queryset(self):
        return SelectionQuerySet(self.model, using=self._db)

    def get_winners(self, game_id, colour):
        return self.get_queryset().get_winners(game_id, colour)

    def get_losers(self, game_id, colour):
        return self.get_queryset().get_losers(game_id, colour)

    def get_reds(self, game_id):
        return self.get_queryset().get_reds(game_id)

    def get_blacks(self, game_id):
        return self.get_queryset().get_blacks(game_id)

class Selection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10, default='', blank=True)
    active = models.BooleanField(default=True, blank=True)
    viewable = models.BooleanField(default=True, blank=True)
    stake = models.IntegerField(default=True, blank=True)
    lost_round = models.IntegerField(default=True, blank=True)

    objects = SelectionManager()

    def set_loser(self, round_no):
        self.active=False
        self.lost_round = round_no
        self.save()

    def reset_winner(self):
        self.colour=""
        self.active=True
        self.save()

    def create_selection(self,selection_form, user_id, game_id):
        self = selection_form.save(commit=False)
        self.player_id = user_id
        self.game_id=game_id
        self.active=True
        self.save()

    def hide_game(self):
        self.viewable=False
        self.save()


    class Meta:
        unique_together = ('game', 'player')
