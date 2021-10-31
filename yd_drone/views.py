from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser

import json
import uuid

from drone_info.settings import MEDIA_ROOT
from yd_drone.models import YDMission, YDLogFile, YDMissionPoint
from yd_drone.bin_parsers import read_mission_bin_file, read_log_bin_file, read_mission_bytes_array


class FlightMissionData(APIView):

    def get(self, request, *args, **kwargs):
        mission = YDMission.objects.get(id=kwargs['id'])
        file_path = MEDIA_ROOT + '/' +mission.flight_mission_file.name
        points = read_mission_bin_file(file_path)
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
            new_mission = self._createMission(data, files)
            self._createMissionPoints(files['mission'], new_mission)
            
        else:
            status = 400
            message = 'Mission with same name already exist'

        return JsonResponse({'message':message}, status=status)

    def _createMission(self, data, files):
        file_name = uuid.uuid4().hex +'.'+ files['mission'].name.split('.')[1]
        files['mission'].name = file_name

        new_mission = YDMission()
        new_mission.mission_name = data['mission_name']
        new_mission.user_info = data['author']
        new_mission.description = data['mission_description']
        new_mission.flight_mission_file = files['mission']
        new_mission.at_create = timezone.now()
        new_mission.save()
        return new_mission
    
    def _createMissionPoints(self, file, mission):
        file.file.seek(0)
        bytes_array = file.file.read()
        points = read_mission_bytes_array(bytes_array)
        for point in points:
            new_point = YDMissionPoint()
            new_point.mission = mission
            new_point.targetLat = point[0]
            new_point.targetLon = point[1]
            new_point.targetAlt = point[2]
            new_point.targetRadius = point[3]
            new_point.loiterTime = point[4]
            new_point.maxHorizSpeed = point[5]
            new_point.maxVertSpeed = point[6]
            new_point.poiLat = point[7]
            new_point.poiLon = point[8]
            new_point.poiHeading = point[9]
            new_point.poiAltitude = point[10]
            new_point.flags = point[11]
            new_point.photo = point[12]
            new_point.panoSectorsCount = point[13]
            new_point.panoDeltaAngle = point[14]
            new_point.poiPitch = point[15]
            new_point.poiRoll = point[16]
            new_point.type = point[17]
            new_point.save()


class FlightMissionHeagers(APIView):
    
    def get(self, request):
        missions = YDMission.objects.all()
        data = json.loads(serializers.serialize('json', missions, fields=('mission_name','user_info','at_create')))
        response = {'result': []}
        for mission in data:
            fields = mission['fields']
            fields['at_create'] = ' '.join(fields['at_create'].split('T'))[:-5]
            log_count = YDLogFile.objects.filter(mission__id=mission['pk']).count()
            fields['log_count'] = log_count
            fields['id'] = mission['pk']
            response['result'].append(fields)
        return JsonResponse(response, status=200)


class MissionLogLoad(APIView):

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
            status = 400
            message = "Миссия с названием '{0}' не существует. Лог можно добавить только к существующей миссии".format(data['mission_name'])
        else:
            new_log = YDLogFile()
            new_log.mission = mission
            new_log.flight_data = data['flight_data']
            new_log.description = data['mission_description']
            new_log.at_create = timezone.now()
            new_log.upload = files['log']
            new_log.save()

        return JsonResponse({'message':message}, status=status) 