from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_annotate.index import vatican_texts_bulk_indexing


class Command(BaseCommand):
    def handle(self, *args, **options):
        vatican_texts_bulk_indexing()
