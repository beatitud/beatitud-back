from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import VerseSerializer
from apps.beatitud_corpus.models import Verse


class VerseViews(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = Verse.objects.order_by('-id').all()
    serializer_class = VerseSerializer
