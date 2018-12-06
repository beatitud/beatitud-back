from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status, viewsets
from .serializers import BibleVerseSerializer, ParamsSerializer
from apps.beatitud_corpus.models import BibleVerse
from utils.elasticsearch_.serializer import EsSerializer
from elasticsearch_dsl import Q, Search
import logging

logger = logging.getLogger(__name__)


def build_search_from_params(params):
    """
    :param params: { "param1": "...", "param2": "...", ...}
    :return: elasticsearch query dict
    """
    must = list()
    filters = list()
    should = list()

    # Filter by app_id
    app_id_list = params.get("app_id", None)
    if app_id_list:
        filters.append(Q('bool', should=[{"term": {"app_id": app_id}} for app_id in app_id_list]))

    # Filter by app_version
    app_version_list = params.get("app_version", None)
    if app_version_list:
        filters.append(Q('bool', should=[{"term": {"app_version": app_version}} for app_version in app_version_list]))

    # Filter by is_pinned
    query_is_pinned = params.get("is_pinned", None)
    if query_is_pinned:
        filters.append(Q('term', is_pinned=query_is_pinned))

    # Filter by is_spam
    query_is_spam = params.get("is_spam", None)
    if query_is_spam:
        filters.append(Q('term', is_spam=query_is_spam))

    # Filter by stars
    query_stars = params.get("stars", None)
    if query_stars:
        filters.append(Q('term', stars=query_stars))

    # Filter by date range
    start = params.get('start', None)
    end = params.get('end', None)
    if start and end:
        filters.append(Q('range', creation_date={
            "gte": start,
            "lte": end,
        }))

    # Filter by persona
    query_persona_id = params.get("persona_id", None)
    if query_persona_id:
        filters.append(Q('term', personas=query_persona_id))

    # Filter by characters length
    char_length_min = params.get('char_length_min', None)
    if char_length_min:
        filters.append(Q('range', len={"gt": char_length_min}))

    # Filter by tags
    query_tags = params.get("tags", None)
    if query_tags:
        for tag in query_tags:
            must.append(Q('term', tags=tag))

    # Filter by query search
    query_search = params.get("query_search", None)
    if query_search:
        must.append(Q('multi_match', query=query_search, fields=["title", "body", "author"]))

    s = Search(index='bible-verse-index')
    s = s.query(Q('bool', must=must, filter=filters, should=should))
    s = s.highlight(fields=["title", "body", "author"], fragment_size=0)

    return s


class BibleVerseViews(APIView):
    permission_classes = ()

    def get(self, request, format=None):
        # We collect params
        request_params = request.query_params.dict()
        # We reformat params list
        query_tags = request.query_params.getlist("tags", None)
        if query_tags:
            request_params.update({"tags": query_tags})
        app_id = request.query_params.getlist("app_id", None)
        if app_id:
            request_params.update({"app_id": app_id})
        app_version = request.query_params.getlist("app_version", None)
        if app_version:
            request_params.update({"app_version": app_version})

        serialized_params = ParamsSerializer(data=request_params)
        if not serialized_params.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, \
                            data={"message": "Error with parameters", "error": serialized_params.errors})

        params = serialized_params.validated_data
        s = build_search_from_params(params)

        # Pagination, to limit quantity of data
        _from = params.get("_from", 0)
        _size = params.get("_size", 15)
        s = s[_from, _from + _size]

        # Order by date
        s = s.sort('-creation_date', )

        search = s.execute()
        verses = EsSerializer(data=search)
        verses = verses["hits"]["hits"]

        # Format data
        for index, review in enumerate(verses):
            verses[index] = review["_source"]
            verses[index]["id"] = int(review["_id"])
            verses[index]["persona"] = verses[index].pop("personas", '')
            if not review.get("highlight", None):
                continue
            if review["highlight"].get("author", None):
                verses[index]["author"] = review["highlight"]["author"][0]
            if review["highlight"].get("title", None):
                verses[index]["title"] = review["highlight"]["title"][0]
            if review["highlight"].get("body", None):
                verses[index]["body"] = review["highlight"]["body"][0]

        # We prepare the data to return
        serialized = BibleVerseSerializer(verses, many=True)

        return Response(status=status.HTTP_200_OK, data=serialized.data)
