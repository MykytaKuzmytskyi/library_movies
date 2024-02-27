from rest_framework import serializers

from movie.models import Actor, Movie, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("id", "first_name", "last_name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "year",
            "directors",
            "actors",
        )


class MovieListSerializer(MovieSerializer):
    directors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Movie
        fields = ("id", "title", "year", "directors", "actors")


class MovieDetailSerializer(MovieSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    directors = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "directors",
            "actors",
        )
