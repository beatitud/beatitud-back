from django.db import models


class Rite(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'rite'
