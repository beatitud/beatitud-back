from django.db import models


class Verse(models.Model):
    verse_nb = models.IntegerField()
    verse = models.TextField()
