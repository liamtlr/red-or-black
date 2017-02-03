from django.db import models
from rob.modeldir.game import *

class Player(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
