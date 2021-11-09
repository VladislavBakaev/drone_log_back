from django.urls import re_path

from yd_drone.views import FlightMissionData, LoadFlightMissionData, FlightMissionHeagers, LoadMissionLog, FlightMissionDataWithParams,\
                           MissionLogDataWithParams

urlpatterns = [
    re_path(r'^mission/(?P<id>\d+)$', FlightMissionData.as_view()),
    re_path(r'^flightmission/load$', LoadFlightMissionData.as_view()),
    re_path(r'^missions/get$', FlightMissionHeagers.as_view()),
    re_path(r'^logs/load$', LoadMissionLog.as_view()),
    re_path(r'^mission$', FlightMissionDataWithParams.as_view()),
    re_path(r'^logs$', MissionLogDataWithParams.as_view())
]