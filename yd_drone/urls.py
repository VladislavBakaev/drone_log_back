from django.conf.urls import url

from yd_drone.views import GetFlightMissionData, LoadFlightMissionData, FlightMissionHeagers, MissionLogLoad

urlpatterns = [
    url(r'flightmission/get$', GetFlightMissionData.as_view()),
    url(r'flightmission/load$', LoadFlightMissionData.as_view()),
    url(r'mission/get$', FlightMissionHeagers.as_view()),
    url(r'logs/load$', MissionLogLoad.as_view())
]