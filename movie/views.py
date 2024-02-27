from rest_framework.viewsets import ModelViewSet

from movie.models import Director, Actor, Movie
from movie.serializers import DirectorSerializer, ActorSerializer, MovieListSerializer, MovieDetailSerializer, \
    MovieSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer

        if self.action == "retrieve":
            return MovieDetailSerializer

        return MovieSerializer
