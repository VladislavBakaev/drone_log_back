from django.contrib import admin
from drone_missions_logs.models import LogFile, Mission, YDMissionPoint, MavLinkPX4MissionPoint

@admin.register(LogFile)
class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'at_create', 'mission', 'flight_data')


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission_name', 'user_info', 'at_create')

@admin.register(YDMissionPoint)
class YDMissionPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission')
    
@admin.register(MavLinkPX4MissionPoint)
class MavLinkPX4MissionPointAdmin(admin.ModelAdmin):
    list_disply = {'id', 'mission'}