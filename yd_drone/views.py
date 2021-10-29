from django.http import JsonResponse
from rest_framework.views import APIView

from drone_info.settings import MEDIA_ROOT
from yd_drone.models import YDMission
from yd_drone.bin_parsers import read_mission_bin_file, read_log_bin_file

class GetFlightMissionData(APIView):

    def get(self, request):
        mission = YDMission.objects.get(id=1)
        file_path = MEDIA_ROOT + '/' +mission.flight_mission_file.name
        points = read_mission_bin_file(file_path)
        return JsonResponse({}, status=200)

class GetMissionLogsData(APIView):
    
    def get(self, request):
        return JsonResponse({}, status=200)