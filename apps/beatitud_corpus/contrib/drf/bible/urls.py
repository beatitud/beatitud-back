from django.conf.urls import url

from .views import VerseViews

urlpatterns = [
    url(r'^verse/$', VerseViews.as_view({'get': 'list'}), name='verse'),
    # url(r'apps/$', get_app_versions, name='reviews-apps'),
    # url(r'tags/$', get_tags, name='tags-reviews'),
]