"""GameRating model module"""
from django.db import models

class GameRating(models.Model):
    """GameRating database model"""
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    gamer_id = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    rating = models.IntegerField()