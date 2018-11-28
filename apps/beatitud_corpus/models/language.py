from django.db import models


class Language(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'language'


class Translation(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=200, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        db_table = 'language_translation'
