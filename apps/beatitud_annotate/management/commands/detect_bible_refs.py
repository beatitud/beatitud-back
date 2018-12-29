from django.core.management.base import BaseCommand, CommandError
from scriptures.text import Text
from apps.beatitud_annotate.models import VaticanText
from utils.scraping.beautiful_soup import BeautifulSoup, get_text_from_bs


class Command(BaseCommand):
    help = 'Fill Vatican Texts'

    def handle(self, *args, **options):
        for vt in VaticanText.objects.iterator():
            print(vt.code)
            # if not vt.verses:
            vt_bs = BeautifulSoup(vt.body, 'html.parser')
            vt_text = get_text_from_bs(vt_bs)
            txt = Text(vt_text, language='fr', canon='catholic')
            bible_refs = txt.extract_refs(guess=True, simplify=True)
            for ref in bible_refs:
                # vt.verses = list(set(map(str, bible_refs)))
                print("{}, {}, {}, {}, {}".format(ref.book, ref.chapter, ref.verse, ref.end_chapter, ref.end_verse))
                print(str(ref))

            # vt.save()
