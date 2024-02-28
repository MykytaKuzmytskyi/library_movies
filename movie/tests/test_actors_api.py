from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from movie.models import Actor
from rest_framework.test import APIClient

from movie.serializers import ActorSerializer

ACTOR_URL = reverse("movie:actor-list")


def detail_url(movie_id):
    return reverse("movie:actor-detail", args=[movie_id])


def create_actors(num_actors):
    for i in range(num_actors):
        actor_data = {"first_name": f"First Name {i}", "last_name": f"Last Name {i}"}
        Actor.objects.create(**actor_data)


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_actor_list(self):
        create_actors(5)

        res = self.client.get(ACTOR_URL)

        actors = Actor.objects.order_by("first_name")
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], len(serializer.data))
        self.assertEqual(res.data["results"], serializer.data)

    def test_get_actor_detail(self):
        create_actors(2)

        url = detail_url(1)
        res = self.client.get(url)

        actors = Actor.objects.get(id=1)
        serializer = ActorSerializer(actors)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_movie_not_allowed(self):
        create_actors(2)

        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }

        res = self.client.put(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_movie_forbidden(self):
        create_actors(2)

        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_get_actor_list(self):
        create_actors(5)

        res = self.client.get(ACTOR_URL)

        actors = Actor.objects.order_by("first_name")
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], len(serializer.data))
        self.assertEqual(res.data["results"], serializer.data)

    def test_get_actor_detail(self):
        create_actors(2)

        url = detail_url(2)
        res = self.client.get(url)

        actors = Actor.objects.get(id=2)
        serializer = ActorSerializer(actors)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_actor(self):
        payload = {
            "first_name": "first",
            "last_name": "last",
        }
        res = self.client.post(ACTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_actor(self):
        create_actors(2)

        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }

        url = detail_url(1)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_actor(self):
        create_actors(2)

        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
