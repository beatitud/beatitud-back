from elasticsearch_dsl import DocType, Integer, Text, Date, Keyword
from utils.elasticsearch_.connector import es_client
from elasticsearch.helpers import bulk, parallel_bulk
from apps.beatitud_annotate.models import VaticanText


class VaticanTextIndex(DocType):
    pope = Text(fielddata=True)
    code = Text(fielddata=True)
    date = Date()
    type = Text(fielddata=True)
    label = Text()
    label2 = Text()
    label3 = Text()
    url = Text()
    multimedia_url = Text()
    headers = Text()
    body = Text()
    language = Text(fielddata=True)
    liturgical_cote = Text(fielddata=True)
    verses = Keyword()

    class Index:
        name = 'vatican-text-index'


def vatican_texts_bulk_indexing():
    bulk(
        client=es_client,
        chunk_size=500,
        actions=(b.indexing(perform_save=False) for b in VaticanText.objects.all().iterator()),
        # thread_count=4,
        stats_only=True,
    )
