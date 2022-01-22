from django.contrib import admin
from drone_missions_logs.models import LogFile, Mission, YDMissionPoint

@admin.register(LogFile)
class LogFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'at_create', 'mission', 'flight_data')


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission_name', 'user_info', 'at_create')

@admin.register(YDMissionPoint)
class YDMissionPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission')