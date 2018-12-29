from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_annotate.models import Pope, VaticanText
from apps.scrapers.vatican.vatican_scraper import VaticanScraper
from apps.beatitud_corpus.models import Language
from django.db.models import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Fill Vatican Texts'

    def handle(self, *args, **options):
        vs = VaticanScraper()
        language = Language.objects.get(code="fr")
        for pope in Pope.objects.filter(has_content=True):
            if pope.code in ['francesco', 'benedict-xvi', 'john-paul-ii']:
                continue
            index_urls = vs.get_index_menu(pope=pope.code, language=language.code)
            for index_url in index_urls:
                index_content = vs.get_index_content(index_url)
                for index_dict in index_content:
                    # If content already exists in db, we skip the url
                    try:
                        VaticanText.objects.get(url=index_dict.get("url"))
                    except ObjectDoesNotExist or Exception:
                        content = vs.get_content(index_dict)
                        if not content:
                            continue
                        VaticanText.objects.create(
                            language=language,
                            pope=pope,
                            date=content.get("date"),
                            label=content.get("label", "")[:300],
                            label2=content.get("label2", "")[:300],
                            label3=content.get("label3", "")[:300],
                            multimedia_url=content.get("multimedia", ""),
                            url=content.get("url"),
                            headers=content.get("headers"),
                            body=content.get("content"),
                            code=content.get("code"),
                            type=content.get("content_type"),
                        )
