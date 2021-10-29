from django.conf.urls import url

from yd_drone.views import GetFlightMissionData

urlpatterns = [
    url(r'flightmission/get$', GetFlightMissionData.as_view())
]