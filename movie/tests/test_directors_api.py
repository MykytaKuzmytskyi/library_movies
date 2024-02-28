from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from movie.models import Director
from rest_framework.test import APIClient

from movie.serializers import DirectorSerializer

DIRECTOR_URL = reverse("movie:director-list")


def detail_url(director_id):
    return reverse("movie:director-detail", args=[director_id])


def create_directors(num_directors):
    for i in range(num_directors):
        actor_data = {
            "first_name": f"First Name {i}",
            "last_name": f"Last Name {i}"
        }
        Director.objects.create(**actor_data)


class UnauthenticatedDirectorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_director_list(self):
        create_directors(5)

        res = self.client.get(DIRECTOR_URL)

        directors = Director.objects.order_by("first_name")
        serializer = DirectorSerializer(directors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], len(serializer.data))
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_director_detail(self):
        create_directors(2)

        url = detail_url(1)
        res = self.client.get(url)

        directors = Director.objects.get(id=1)
        serializer = DirectorSerializer(directors)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_director_forbidden(self):
        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }
        res = self.client.post(DIRECTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_director_not_allowed(self):
        create_directors(2)

        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }

        res = self.client.put(DIRECTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_director_forbidden(self):
        create_directors(2)

        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminDirectorApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_get_director_list(self):
        create_directors(5)

        res = self.client.get(DIRECTOR_URL)

        directors = Director.objects.order_by("first_name")
        serializer = DirectorSerializer(directors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], len(serializer.data))
        self.assertEqual(res.data['results'], serializer.data)

    def test_get_director_detail(self):
        create_directors(2)

        url = detail_url(2)
        res = self.client.get(url)

        actors = Director.objects.get(id=2)
        serializer = DirectorSerializer(actors)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_actor(self):
        payload = {
            "first_name": "first",
            "last_name": "last",
        }
        res = self.client.post(DIRECTOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_actor(self):
        create_directors(2)

        payload = {
            "first_name": "first_name",
            "last_name": "last_name",
        }

        url = detail_url(1)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_actor(self):
        create_directors(2)

        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
