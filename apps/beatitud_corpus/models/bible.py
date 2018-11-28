from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch_dsl import DocType, Integer, Keyword, Text, Date, Boolean, Float, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from apps.beatitud_corpus.contrib.elasticsearch import *
from .language import Language


class Book(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.TextField(db_index=True)

    class Meta:
        db_table = 'bible_book'


class Verse(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    verse_id = models.CharField(null=False, unique=True, max_length=50, db_index=True)
    verse_nb = models.IntegerField(db_index=True)
    text = models.TextField()
    text_introductory = models.TextField()
    text_ending = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'bible_verse'

    def indexing(self):
        obj = VerseIndex(
            meta={'id': self.id},
            id=self.id,
            verse_id=self.verse_id,
            text=self.text,
            text_introductory=self.text_introductory,
            text_ending=self.text_ending,
            book=list(self.book.name),
            len=len(self.text),
        )
        obj.save(index='review-index')
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=Verse)
def index_post(sender, instance, **kwargs):
    instance.indexing()


class VerseIndex(DocType):
    verse_id = Text()
    verse_nb = Integer()
    text = Text()
    text_introductory = Text()
    text_ending = Text()
    book = Text(fielddata=True)
    len = Integer()

    class Meta:
        index = 'bible-verse-index'


def bulk_indexing():
    VerseIndex.init(index=VerseIndex.Meta.index)
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in Verse.objects.all().iterator()))
