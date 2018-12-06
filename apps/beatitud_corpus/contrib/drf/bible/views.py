from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from .serializers import BibleVerseSerializer
from apps.beatitud_corpus.models import BibleVerse


class BibleVerseViews(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = BibleVerse.objects.order_by('-id').all()
    serializer_class = BibleVerseSerializer
