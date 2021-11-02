from django.db import models
from django.db.models.base import Model

# Create your models here.
class Game(models.Model):
    subject = models.CharField(max_length=200)
    create_date = models.DateTimeField()

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    create_date = models.DateTimeField()
