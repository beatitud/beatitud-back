from rest_framework import serializers


class ReadingsParams(serializers.Serializer):

    version = serializers.CharField()
    date = serializers.DateField()