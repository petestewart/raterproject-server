"""GameReview model module"""
from django.db import models

class GameReview(models.Model):
    """GameReview database model"""
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    gamer_id = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    review = models.IntegerField()