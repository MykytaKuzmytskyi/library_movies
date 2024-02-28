from random import randint

from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from django.test import TestCase
from rest_framework import status

from movie.models import Actor, Director, Movie
from rest_framework.test import APIClient

from movie.serializers import MovieListSerializer, MovieDetailSerializer

MOVIE_URL = reverse("movie:movie-list")


def detail_url(movie_id):
    return reverse("movie:movie-detail", args=[movie_id])


def create_movies(num_movies):
    with transaction.atomic():
        for num in range(num_movies):
            actor1 = Actor.objects.create(first_name=f"A {num}", last_name=f"B {num}")
            actor2 = Actor.objects.create(first_name=f"C {num}", last_name=f"D {num}")

            director = Director.objects.create(
                first_name=f"A {num}", last_name=f"B {num}"
            )
            movie = Movie.objects.create(
                title=f"Title {num}",
                year=1900 + num,
            )

            movie.actors.add(actor1, actor2)
            movie.directors.add(director)


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_movie_list(self):
        create_movies(15)

        movies = Movie.objects.order_by("id")
        serializer = MovieListSerializer(movies, many=True)

        res = self.client.get(MOVIE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], len(serializer.data))

    def test_filter_by_year(self):
        create_movies(15)

        res = self.client.get(MOVIE_URL, {"year": 1901})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_filter_by_directors(self):
        create_movies(5)

        res = self.client.get(MOVIE_URL, {"directors__first_name": "A 1"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_filter_by_actors(self):
        create_movies(5)

        res = self.client.get(MOVIE_URL, {"actors__first_name": "A 1"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_get_movie_detail(self):
        create_movies(1)
        url = detail_url(1)
        res = self.client.get(url)

        movie = Movie.objects.get(id=1)
        serializer = MovieDetailSerializer(movie)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        payload = {
            "title": "tile",
            "year": 2020,
        }
        res = self.client.post(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_movie_not_allowed(self):
        payload = {
            "title": "tile",
            "year": 2020,
        }

        res = self.client.put(MOVIE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_movie_forbidden(self):
        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_movie(self):
        actor = Actor.objects.create(first_name="A", last_name="B")
        director = Director.objects.create(first_name="A", last_name="B")
        payload = {
            "title": "tile",
            "year": 2020,
            "actors": [actor.id],
            "directors": [director.id],
        }

        res = self.client.post(MOVIE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_movie(self):
        create_movies(2)
        payload = {
            "title": "tile",
            "year": 2020,
        }

        url = detail_url(1)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_movie(self):
        create_movies(2)

        url = detail_url(1)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
