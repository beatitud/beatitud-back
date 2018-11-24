from django.urls import path, include

urlpatterns = [
    path('', include('apps.beatitud_corpus.contrib.drf.daily_readings.urls')),
    path('', include('apps.beatitud_corpus.contrib.drf.saints.urls')),
    path('', include('apps.beatitud_corpus.contrib.drf.bible.urls')),
    path('', include('apps.beatitud_corpus.contrib.drf.users.urls')),
]