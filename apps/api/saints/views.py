from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class ReadingsViews(APIView):
    def get(self, request, format=None):
        # We serialize params
        serialized_params = ReadingsParams(data=request.query_params)

        if not serialized_params.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "Error with parameters", "error": serialized_params.errors})

        params = serialized_params.validated_data
        version = params.get("version")
        date = params.get("date")
        url = "{}/{}/days/{}/readings".format(EVZOBASEURL, version, date)

        return requests.get(url=url)
