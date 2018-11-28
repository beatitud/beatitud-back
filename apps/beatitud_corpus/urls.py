from django.urls import path, include

urlpatterns = [
    path('daily-readings/', include('apps.beatitud_corpus.contrib.drf.daily_readings.urls')),
    path('saint/', include('apps.beatitud_corpus.contrib.drf.saint.urls')),
    path('bible/', include('apps.beatitud_corpus.contrib.drf.bible.urls')),
]