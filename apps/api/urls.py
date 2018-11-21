from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url('^readings/', include('data.api.readings.urls')),

]

urlpatterns += router.urls