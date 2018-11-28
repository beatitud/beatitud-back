from django.db import models
from django.contrib.postgres.fields import ArrayField
from .language import Language


class Saint(models.Model):
    BLESSED = 'bl'
    SAINT = 'st'
    STATUS_CHOICES = (
        (BLESSED, 'Blessed'),
        (SAINT, 'Saint'),
    )
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True)
    feast_date = models.DateField(null=True)
    pictures = ArrayField(models.URLField(), null=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=SAINT)

    class Meta:
        db_table = 'saint'


class Hagiography(models.Model):
    title = models.TextField()
    body = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE)

    class Meta:
        db_table = 'saint_hagiography'
