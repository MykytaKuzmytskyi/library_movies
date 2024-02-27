from django.urls import path, include
from rest_framework import routers

from movie.views import (
    ActorViewSet, DirectorViewSet, MovieViewSet
)

router = routers.DefaultRouter()
router.register("director", DirectorViewSet)
router.register("actors", ActorViewSet)
router.register("movies", MovieViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "cinema"
