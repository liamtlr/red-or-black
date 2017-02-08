from django.db import models
from rob.modeldir.player import *
from rob.modeldir.game import *

class Selection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10, default='', blank=True)
    active = models.BooleanField(default=True, blank=True)
    viewable = models.BooleanField(default=True, blank=True)
    stake = models.IntegerField(default=True, blank=True)
    lost_round = models.IntegerField(default=True, blank=True)

    def set_loser(self, round_no):
        self.active=False
        self.lost_round = round_no
        self.save()

    def reset_winners(self):
        self.colour=""
        self.active=True
        self.save()

    class Meta:
        unique_together = ('game', 'player')
