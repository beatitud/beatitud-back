from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_annotate.models import Pope
from apps.scrapers.vatican.vatican_scraper import VaticanScraper
from apps.beatitud_corpus.models import Language


class Command(BaseCommand):
    help = 'Fill popes'

    def handle(self, *args, **options):
        vs = VaticanScraper()
        language = Language.objects.get(code="fr")
        popes = vs.get_popes(language=language.code)
        for pope in popes:
            Pope.objects.get_or_create(
                code=pope.get("code"),
                name=pope.get("name"),
                subtitle=pope.get("subtitle"),
                has_content=pope.get("has_content"),
                language=language,
            )
