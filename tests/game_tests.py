import json
from rest_framework import status
from rest_framework.test import APITestCase
from raterprojectapi.models import Game

class GameTests(APITestCase):
    def setUp(self):
        """Create a new account and create sample category"""

        url = "/register"
        data = {
            "username": "pete",
            "password": "Admin8*",
            "email": "pete@pete.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Pete",
            "last_name": "Stewart",
            "bio": "Love this bio!!"
        }

        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created (check if these two things are equal)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_game(self):
        """Ensure we can create a game"""

        # Define game properties
        url = "/games"
        data = {
            "title": "Clue",
            "description": "who did it?",
            "year_released": 1955,
            "number_of_players": 5,
            "estimated_time": 1,
            "minimum_age": 12
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["description"], "who did it?")
        self.assertEqual(json_response["year_released"], 1955)
        self.assertEqual(json_response["number_of_players"], 5)
        self.assertEqual(json_response["estimated_time"], 1)
        self.assertEqual(json_response["minimum_age"], 12)
        
    def test_modify_game(self):
        """Ensure we can modify a game"""

        game = Game()
        game.title = "Clue"
        game.description = "who did it?"
        game.year_released = 1955
        game.number_of_players = 5
        game.estimated_time = 5
        game.minimum_age = 12
        game.gamer_id = 1
        game.save()

        # Define new properties for game
        data = {
            "title": "Sorry",
            "description": "old board game",
            "year_released": 1960,
            "number_of_players": 4,
            "estimated_time": 2,
            "minimum_age": 6
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get Game to verify changes
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["description"], "old board game")
        self.assertEqual(json_response["year_released"], 1960)
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["estimated_time"], 2)
        self.assertEqual(json_response["minimum_age"], 6)

    def test_delete_game(self):
        """Ensure we can delete a game"""

        game = Game()
        game.title = "Clue"
        game.description = "who did it?",
        game.year_released = 1955
        game.number_of_players = 5
        game.estimated_time = 5
        game.minimum_age = 12
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get game to verify 404 response
        response = self.client.get(f"games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_game(self):
        """Ensure we can get a single game"""

        # Seed the database with a game
        game = Game()
        game.title = "Clue"
        game.description = "who did it?"
        game.year_released = 1955
        game.number_of_players = 5
        game.estimated_time = 5
        game.minimum_age = 12
        game.gamer_id = 1
        game.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that values are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["description"], "who did it?")
        self.assertEqual(json_response["year_released"], 1955)
        self.assertEqual(json_response["number_of_players"], 5)
        self.assertEqual(json_response["estimated_time"], 5)
        self.assertEqual(json_response["minimum_age"], 12)