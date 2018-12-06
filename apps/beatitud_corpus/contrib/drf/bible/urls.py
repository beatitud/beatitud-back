from django.conf.urls import url

from .views import BibleVerseViews

urlpatterns = [
    url(r'^verse/$', BibleVerseViews.as_view(), name='verse'),
    # url(r'apps/$', get_app_versions, name='reviews-apps'),
    # url(r'tags/$', get_tags, name='tags-reviews'),
]