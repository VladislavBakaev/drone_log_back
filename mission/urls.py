from django.conf.urls import url

from mission.views import TestApi

urlpatterns = [
    url(r'add$', TestApi.as_view())
]