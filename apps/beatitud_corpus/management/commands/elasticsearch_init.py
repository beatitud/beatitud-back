from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_corpus.index import BibleVerseIndex


class Command(BaseCommand):
    help = 'Init Elasticsearch Index'

    def handle(self, *args, **options):
        BibleVerseIndex.init()
