from elasticsearch_dsl import DocType, Integer, Text
from utils.elasticsearch_.connector import *
from utils.elasticsearch_ import bulk, Elasticsearch
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
    BibleVerseIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in BibleVerse.objects.all().iterator()))
