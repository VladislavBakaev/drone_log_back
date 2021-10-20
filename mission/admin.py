from django.contrib import admin
from mission.models import Mission, Point, UserInfo


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission_name', 'user_info', 'at_create')


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission' ,'param1', 'param2', 'param3', 'param4',\
                    'x', 'y', 'z', 'seq', 'command', 'target_system',\
                    'target_component', 'frame', 'current',\
                    'autocontinue', 'mission_type')


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'system_user_name', 'ip_address',\
                    'operation_system','ardupilot_version')
