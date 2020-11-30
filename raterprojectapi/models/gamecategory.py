"""GameCategory model module"""
from django.db import models

class GameCategory(models.Model):
    """GameCategory database model"""
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
