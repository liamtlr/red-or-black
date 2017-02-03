from django.db import models
from rob.modeldir.player import *
from rob.modeldir.game import *

class Selection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10, default='', blank=True)

    class Meta:
        unique_together = ('game', 'player')
