from apps.beatitud_corpus.models import BibleVerse
from rest_framework import serializers

__all__ = ['BibleVerseSerializer', 'ParamsSerializer']


class BibleVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BibleVerse
        exclude = []


class ParamsSerializer(serializers.Serializer):
    app_id = serializers.ListField(required=False, child=serializers.IntegerField())
    app_version = serializers.ListField(required=False, child=serializers.CharField())
    is_pinned = serializers.BooleanField(required=False)
    is_spam = serializers.CharField(required=False)
    stars = serializers.CharField(required=False)
    query_search = serializers.CharField(required=False)
    tags = serializers.ListField(required=False)
    _from = serializers.IntegerField(required=False)
    _size = serializers.IntegerField(required=False)
    char_length_min = serializers.IntegerField(required=False)
    persona_id = serializers.IntegerField(required=False)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
