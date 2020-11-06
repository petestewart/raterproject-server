"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Game, Gamer
from django.contrib.auth.models import User

class Games(ViewSet):
    """Rater games"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            # designer = User.objects.get(pk=game.gamer_id)
            # game.designer = designer

            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        gamer = Gamer.objects.get(user=request.auth.user)

        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.year_released = request.data["year_released"]
        game.number_of_players = request.data["number_of_players"]
        game.estimated_time = request.data["estimated_time"]
        game.minimum_age = request.data["minimum_age"]
        game.gamer = gamer

        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET resquests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from teh database
        games = Game.objects.all()

        # Support filtering games by type
        #   http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(gametype__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


class GameUserSerializer(serializers.ModelSerializer):
    """JSON serializer for game designer's related Django user"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class GameDesignerSerializer(serializers.ModelSerializer):
    """JSON serializer for game designer"""
    user = GameUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    gamer = GameDesignerSerializer(many=False)

    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'description', 'year_released','number_of_players', 'estimated_time', 'minimum_age', 'gamer')
        depth = 1
