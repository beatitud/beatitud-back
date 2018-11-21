from django.conf.urls import url

from .views import ReadingsViews

urlpatterns = [
    url(r'^daily-readings/$', ReadingsViews.as_view(), name='readings'),
    # url(r'apps/$', get_app_versions, name='reviews-apps'),
    # url(r'tags/$', get_tags, name='tags-reviews'),
]