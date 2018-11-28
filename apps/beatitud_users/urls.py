from django.urls import path, include

urlpatterns = [
    path('', include('apps.beatitud_users.contrib.drf.users.urls')),
]
