from apps.beatitud_corpus.models import BibleVerse
from rest_framework import serializers

__all__ = ['BibleVerseSerializer',]


class BibleVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleVerse
        exclude = []
