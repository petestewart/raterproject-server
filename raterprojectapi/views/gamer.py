"""View module for handling requests about games"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from raterprojectapi.models import Gamer

class Gamers(ViewSet):
    """Rater gamers"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single gamer

        Returns:
            Response -- JSON serialized gamer instance
        """
        try:
            # `pk` is a parameter to this function, and Django parses it from the URL route parameter
            #   http://localhost:8000/gamers/2
            #
            # The `2` at the end of the route becomes `pk`
            gamer = Gamer.objects.get(pk=pk)
            serializer = GamerSerializer(gamer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized gamer instance
        """

        gamer = Gamer()
        gamer.bio = request.data["bio"]

        try:
            gamer.save()
            serializer = GamerSerializer(gamer, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET resquests to gamers resource

        Returns:
            Response -- JSON serialized list of gamers
        """
        # Get all game records from teh database
        gamers = Gamer.objects.all()

        # Support filtering games by type
        #   http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        
        serializer = GamerSerializer(
            gamers, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for related user"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class GamerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for gamers
    """

    class Meta:
        model = Gamer
        url = serializers.HyperlinkedIdentityField(
            view_name='gamer',
            lookup_field='id'
        )
        fields = ('id', 'bio', 'url')
        depth = 1
