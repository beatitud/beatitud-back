from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from elasticsearch_dsl import DocType, Integer, Text
from utils.elasticsearch_ import *
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from .language import Language, Translation


class Book(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.TextField(db_index=True)

    class Meta:
        db_table = 'bible_book'


class Verse(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    verse_id = models.CharField(null=False, unique=True, max_length=50, db_index=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter = models.IntegerField(db_index=True, null=True)
    number = models.IntegerField(db_index=True, null=True)
    text = models.TextField()
    text_introductory = models.TextField()
    text_ending = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'bible_verse'

    def indexing(self):
        obj = VerseIndex(
            meta={'id': self.id},
            id=self.id,
            verse_id=self.verse_id,
            book=self.book.name,
            chapter=self.chapter,
            number=self.number,
            text=self.text,
            text_introductory=self.text_introductory,
            text_ending=self.text_ending,
            language=self.language.code,
            translation=self.translation.code,
            len=len(self.text),
        )
        obj.save(index='review-index')
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=Verse)
def index_post(sender, instance, **kwargs):
    instance.indexing()


class VerseIndex(DocType):
    verse_id = Text(fielddata=True)
    book = Text(fielddata=True)
    chapter = Text(fielddata=True)
    number = Integer(fielddata=True)
    text = Text()
    text_introductory = Text()
    text_ending = Text()
    language = Text(fielddata=True)
    translation = Text(fielddata=True)
    len = Integer()

    class Meta:
        index = 'bible-verse-index'


def bulk_indexing():
    VerseIndex.init(index=VerseIndex.Meta.index)
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in Verse.objects.all().iterator()))
