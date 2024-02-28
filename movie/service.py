import django_filters

from movie.models import Movie


class MovieFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        field_name="year", label="Year", lookup_expr="exact"
    )

    directors__first_name = django_filters.CharFilter(
        field_name="directors__first_name",
        lookup_expr="icontains",
        label="Director First Name:",
    )
    directors__last_name = django_filters.CharFilter(
        field_name="directors__last_name",
        lookup_expr="icontains",
        label="Director Second Name:",
    )

    actors__first_name = django_filters.CharFilter(
        field_name="actors__first_name",
        lookup_expr="icontains",
        label="Actor First Name:",
    )

    actors__second_name = django_filters.CharFilter(
        field_name="actors__second_name",
        lookup_expr="icontains",
        label="Actor First Name:",
    )

    class Meta:
        model = Movie
        fields = [
            "year",
            "directors__first_name",
            "directors__last_name",
            "actors__first_name",
            "actors__second_name",
        ]
