from rest_framework.viewsets import ModelViewSet

from movie.models import Director, Actor
from movie.serializers import DirectorSerializer, ActorSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
