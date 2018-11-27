from django.conf.urls import url

from .views import SaintsViews

urlpatterns = [
    url(r'^$', SaintsViews.as_view(), name='saints'),
    # url(r'apps/$', get_app_versions, name='reviews-apps'),
    # url(r'tags/$', get_tags, name='tags-reviews'),
]