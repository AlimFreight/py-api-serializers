from rest_framework import serializers

from cinema import models
from cinema.models import MovieSession


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Actor
        fields = ("id", "first_name", "last_name", "full_name",)


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = "__all__"


class GenreViewSerializer(GenreSerializer):
    pass


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = "__all__"


class MovieListSerializer(MovieSerializer):
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class MovieDetailSerializer(MovieSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionDetailSerializer(MovieSessionSerializer):
    movie = MovieListSerializer(many=False, read_only=True)
    cinema_hall = CinemaHallSerializer(many=False, read_only=True)


class MovieSessionListSerializer(MovieSessionSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name",
        read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity",
        read_only=True
    )

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity"
        )
