"""Game model module"""
from django.db import models

class Game(models.Model):
    """Game database model"""
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    estimated_time = models.IntegerField()
    minimum_age = models.IntegerField()