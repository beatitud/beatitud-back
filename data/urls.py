from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api/', include('data.api.urls')),
]
