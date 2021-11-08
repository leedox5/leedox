from django.db import models
from django.db.models.base import Model

# Create your models here.
class Game(models.Model):
    subject = models.CharField(max_length=200)
    create_date = models.DateTimeField()

class Player(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    score_01 = models.IntegerField(null=True)
    score_02 = models.IntegerField(null=True)
    score_03 = models.IntegerField(null=True)
    score_04 = models.IntegerField(null=True)
    score_11 = models.IntegerField(null=True)
    score_12 = models.IntegerField(null=True)
    score_13 = models.IntegerField(null=True)
    score_14 = models.IntegerField(null=True)
    win_ma = models.IntegerField(null=True)
    los_ma = models.IntegerField(null=True)
    win_ga = models.IntegerField(null=True)
    los_ga = models.IntegerField(null=True)
    sum_ga = models.IntegerField(null=True)
    game_rank = models.IntegerField(null=True)
    create_date = models.DateTimeField()

class Match(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player1 = models.ForeignKey(Player, related_name="p1_match", on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name="p2_match", on_delete=models.CASCADE)
    player3 = models.ForeignKey(Player, related_name="p3_match", on_delete=models.CASCADE)
    player4 = models.ForeignKey(Player, related_name="p4_match", on_delete=models.CASCADE)
    seq = models.IntegerField()
    desc = models.CharField(max_length=200)
    score = models.CharField(max_length=20)
    create_date = models.DateTimeField()
    