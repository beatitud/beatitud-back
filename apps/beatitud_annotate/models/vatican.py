from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.beatitud_corpus.models import Language
from utils.scraping.beautiful_soup import get_text_from_bs, BeautifulSoup
from django.db.models.signals import post_save
from django.dispatch import receiver


class Pope(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(max_length=30, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    subtitle = models.CharField(max_length=200)
    has_content = models.BooleanField(default=False)

    class Meta:
        db_table = 'vatican_pope'


class VaticanText(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    pope = models.ForeignKey(Pope, on_delete=models.CASCADE)
    code = models.CharField(max_length=300)
    date = models.DateField()
    type = models.CharField(max_length=50)
    label = models.CharField(max_length=300)
    label2 = models.CharField(max_length=300)
    label3 = models.CharField(max_length=300)
    url = models.URLField(null=True, unique=True, db_index=True, max_length=300)
    multimedia_url = models.URLField(null=True, max_length=300)
    headers = models.TextField(null=True)
    body = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    liturgical_cote = models.CharField(max_length=20, null=True)
    verses = ArrayField(models.CharField(max_length=20), null=True)

    class Meta:
        db_table = 'vatican_text'

    def indexing(self, perform_save=True):
        from apps.beatitud_annotate.index import VaticanTextIndex
        obj = VaticanTextIndex(
            meta={'id': self.id},
            id=self.id,
            pope=self.pope.code,
            code=self.code,
            date=self.date,
            type=self.type,
            label=self.label,
            label2=self.label2,
            label3=self.label3,
            url=self.url,
            multimedia_url=self.multimedia_url,
            headers=self.headers,
            body=get_text_from_bs(BeautifulSoup(self.body, 'html.parser')),
            language=self.language.code,
            liturgical_cote=self.liturgical_cote,
            verses=self.verses,
        )
        if perform_save:
            obj.save()
        return obj.to_dict(include_meta=True)


@receiver(post_save, sender=VaticanText)
def index_post(sender, instance, **kwargs):
    instance.indexing()
