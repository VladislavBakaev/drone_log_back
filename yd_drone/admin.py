from django.contrib import admin
from yd_drone.models import YDLogFile, YDMission, YDMissionPoint

@admin.register(YDLogFile)
class YDLogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'at_create', 'mission', 'flight_data')


@admin.register(YDMission)
class YDMissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission_name', 'user_info', 'at_create')

@admin.register(YDMissionPoint)
class YDMissionPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission')