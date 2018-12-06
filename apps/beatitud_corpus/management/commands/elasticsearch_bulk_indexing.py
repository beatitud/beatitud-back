from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_corpus.index import bible_verse_bulk_indexing


class Command(BaseCommand):
    help = 'Init Elasticsearch Index'

    def handle(self, *args, **options):
        bible_verse_bulk_indexing()
