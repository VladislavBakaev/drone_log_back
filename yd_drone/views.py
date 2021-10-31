from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser

import json
import uuid

from drone_info.settings import MEDIA_ROOT
from yd_drone.models import YDMission, YDLogFile
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


class LoadFlightMissionData(APIView):
    
    parser_class = [JSONParser, FileUploadParser]
    
    def post(self, request):
        files = request.FILES
        data = json.loads(request.data['info'])

        status = 200
        message = 'Success'

        try:
            mission = YDMission.objects.get(mission_name=data['mission_name'])
        except ObjectDoesNotExist:
            mission = None
        
        if mission is None:
            file_name = uuid.uuid4().hex +'.'+ files['mission'].name.split('.')[1]
            files['mission'].name = file_name

            new_mission = YDMission()
            new_mission.mission_name = data['mission_name']
            new_mission.user_info = data['author']
            new_mission.description = data['mission_description']
            new_mission.flight_mission_file = files['mission']
            new_mission.at_create = timezone.now()
            new_mission.save()
        else:
            status = 400
            message = 'Mission with same name already exist'

        return JsonResponse({'message':message}, status=status) 


class FlightMissionHeagers(APIView):
    
    def get(self, request):
        missions = YDMission.objects.all()
        data = json.loads(serializers.serialize('json', missions, fields=('mission_name','user_info','at_create')))
        response = {'result': []}
        for mission in data:
            fields = mission['fields']
            fields['at_create'] = ' '.join(fields['at_create'].split('T'))[:-5]
            response['result'].append(fields)
        return JsonResponse(response, status=200)


class MissionLogLoad(APIView):

    def post(self, request):
        files = request.FILES
        data = json.loads(request.data['info'])

        status = 200
        message = 'Success'

        return JsonResponse({'message':message}, status=status) 