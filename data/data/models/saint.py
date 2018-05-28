from django.db import models


class Saint(models.Model):
    verse_nb = models.IntegerField()
    verse = models.TextField()

    class Meta:
        db_table = 'saint'
