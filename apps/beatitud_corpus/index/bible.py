from elasticsearch_dsl import DocType, Integer, Text
from utils.elasticsearch_.connector import es_client
from elasticsearch.helpers import bulk, parallel_bulk
from apps.beatitud_corpus.models import BibleVerse


class BibleVerseIndex(DocType):
    ref = Text(fielddata=True)
    book = Text(fielddata=True)
    chapter = Text(fielddata=True)
    number = Integer()
    text = Text()
    text_introductory = Text()
    text_ending = Text()
    language = Text(fielddata=True)
    version = Text(fielddata=True)
    len = Integer()

    class Index:
        name = 'bible-verse-index'


def bible_verse_bulk_indexing():
    # BibleVerseIndex.init('bible-verse-index')
    bulk(
        client=es_client,
        chunk_size=500,
        actions=(b.indexing(perform_save=False) for b in BibleVerse.objects.all().iterator()),
        # thread_count=4,
        stats_only=True,
    )
