from django.conf.urls import url

from apps.beatitud_corpus.contrib.drf.bible.views import BibleVerseViews
from apps.beatitud_corpus.contrib.drf.daily_readings.views import ReadingsViews
from apps.beatitud_corpus.contrib.drf.saint.views import SaintsViews

urlpatterns = [
    url(r'^bible/verse/$', BibleVerseViews.as_view(), name='verse'),
    url(r'^daily-readings/$', ReadingsViews.as_view(), name='readings'),
    url(r'^saint/$', SaintsViews.as_view(), name='saints'),
]