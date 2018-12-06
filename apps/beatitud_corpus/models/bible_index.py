from elasticsearch_dsl import DocType, Integer, Text
from utils.elasticsearch_.connector import *


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


# def bulk_indexing():
#     BibleVerseIndex.init(index=BibleVerseIndex.Meta.index)
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in BibleVerse.objects.all().iterator()))
