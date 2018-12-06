from django.core.management.base import BaseCommand, CommandError
from apps.beatitud_corpus.models import BibleVerseRef, BibleVerse, BibleBook, BibleVersion
import json
import progressbar


class Command(BaseCommand):
    help = 'Upload bible verses in db'

    def handle(self, *args, **options):
        with open('./data/bible_verses.json', "r") as f:
            verses = json.load(f)

        with open('./data/bible_refs_list.json', "r") as f:
            refs = json.load(f)

        over = False
        book = None
        versions = {
            "bj": BibleVersion.objects.get_or_create(code="bj")[0],
            "bfc": BibleVersion.objects.get_or_create(code="bfc")[0],
            "tob": BibleVersion.objects.get_or_create(code="tob")[0],
        }
        bar = progressbar.ProgressBar()
        for ref in bar(refs):
            if ref == "eze_20_8":
                over = True
            if not over:
                continue
            verse = verses.get(ref)
            if not book or verse.get("book") != book.code:
                book, is_created = BibleBook.objects.get_or_create(
                    code=verse.get("book")
                )
            ref_obj, is_created = BibleVerseRef.objects.get_or_create(
                code=verse.get("ref_bj"),
                book=book,
                chapter=int(verse.get("chapter")),
                number=int(verse.get("verse")),
            )
            for version, version_obj in versions.items():
                text = verse.get("text_{}".format(version))
                if not text:
                    continue
                BibleVerse.objects.get_or_create(
                    ref=ref_obj,
                    version=version_obj,
                    text=text,
                    text_introductory="",
                    text_ending="",
                )
