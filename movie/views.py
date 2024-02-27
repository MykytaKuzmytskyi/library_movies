from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from movie.models import Director, Actor, Movie
from movie.serializers import DirectorSerializer, ActorSerializer, MovieListSerializer, MovieDetailSerializer, \
    MovieSerializer
from movie.service import MovieFilter


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "delete"]:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "delete"]:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer

        if self.action == "retrieve":
            return MovieDetailSerializer

        return MovieSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "delete"]:
            self.permission_classes = [IsAdminUser, ]
        return super().get_permissions()
