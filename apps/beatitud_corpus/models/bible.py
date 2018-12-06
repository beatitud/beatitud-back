from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .language import Language, Translation


class BibleVersion(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(db_index=True, max_length=30)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'bible_version'


class BibleBook(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.TextField(db_index=True)
    chapter_count = models.IntegerField(null=True)

    class Meta:
        db_table = 'bible_book'


class BibleVerseRef(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(db_index=True, max_length=30)
    book = models.ForeignKey(BibleBook, on_delete=models.CASCADE)
    chapter = models.IntegerField(db_index=True, null=True)
    number = models.IntegerField(db_index=True, null=True)

    class Meta:
        db_table = 'bible_verse_ref'


class BibleVerse(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    ref = models.ForeignKey(BibleVerseRef, on_delete=models.CASCADE, null=True)
    version = models.ForeignKey(BibleVersion, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    text_introductory = models.TextField(null=True)
    text_ending = models.TextField(null=True)

    class Meta:
        db_table = 'bible_verse'

    def indexing(self):
        from apps.beatitud_corpus.models import BibleVerseIndex
        obj = BibleVerseIndex(
            meta={'id': self.id},
            id=self.id,
            ref=self.ref.code,
            book=self.ref.book.code,
            chapter=self.ref.chapter,
            number=self.ref.number,
            text=self.text,
            text_introductory=self.text_introductory,
            text_ending=self.text_ending,
            language=self.version.language.code,
            version=self.version.code,
            len=len(self.text),
        )
        obj.save()
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=BibleVerse)
def index_post(sender, instance, **kwargs):
    instance.indexing()
