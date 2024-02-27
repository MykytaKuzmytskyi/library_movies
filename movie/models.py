from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        abstract = True
        unique_together = ('first_name', 'last_name',)
        ordering = ("first_name", )

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Director(Person):
    pass


class Actor(Person):
    pass


class Movie(models.Model):
    title = models.CharField(max_length=2550)
    year = models.PositiveIntegerField()
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return f"{self.title} - ({self.year})"

    class Meta:
        unique_together = ('title', 'year',)
