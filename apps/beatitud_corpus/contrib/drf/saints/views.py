from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class SaintsViews(APIView):
    def get(self, request, format=None):

        return Response(data={"data": "I am a saint"}, status=status.HTTP_200_OK)
