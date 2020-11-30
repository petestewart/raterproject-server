"""View module for handling requests about gamecategories"""
from raterprojectapi.models import gamecategory
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import GameCategory, Game, Category

class GameCategories(ViewSet):
    """Rater game-categories join table"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response
        """
        game = Game.objects.get(pk=request.data["game_id"])
        category = Category.objects.get(pk=request.data["category_id"])

        gamecategory = GameCategory()
        gamecategory.game = game
        gamecategory.category = category

        try:
            gamecategory.save()
            serializer = GameCategorySerializer(gamecategory, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game-category response"""

    class Meta:
        model = GameCategory
        fields = ('id', 'game_id', 'category_id')
        depth = 1