from apps.beatitud_corpus.models import Verse
from rest_framework import serializers

__all__ = ['VerseSerializer',]


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        exclude = []
