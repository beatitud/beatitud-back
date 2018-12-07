from django.urls import path, include

urlpatterns = [
    path('', include('apps.beatitud_corpus.contrib.drf.urls')),
]