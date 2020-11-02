"""GamePic model module"""
from django.db import models

class GamePic(models.Model):
    """GamePic database model"""
    game_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    gamer_id = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    pic_url = models.URLField()