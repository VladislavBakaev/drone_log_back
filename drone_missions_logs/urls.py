from django.urls import re_path

from drone_missions_logs.views import MissionView, MissionDataLoad, MissionViewAll, LogDataLoad, \
                                      MissionViewWithParams, LogViewWithParams

urlpatterns = [
    re_path(r'^mission/(?P<id>\d+)$', MissionView.as_view()),
    re_path(r'^mission/all$', MissionViewAll.as_view()),
    
    re_path(r'^mission/load$', MissionDataLoad.as_view()),
    re_path(r'^mission/get$', MissionViewWithParams.as_view()),
    
    re_path(r'^log/load$', LogDataLoad.as_view()),
    re_path(r'^log/get$', LogViewWithParams.as_view())
]