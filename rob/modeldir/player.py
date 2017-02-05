from django.db import models
from rob.modeldir.game import *

class Player(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    credits = models.IntegerField(default=10, blank=True)
    lost_round = models.IntegerField(null=True, blank=True, default=0)
