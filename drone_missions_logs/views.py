from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser

import json
import uuid

from drone_info.settings import MEDIA_ROOT
from drone_missions_logs.models import Mission, LogFile, YDMissionPoint
from drone_missions_logs.bin_parsers import read_mission_bytes_array, read_log_bin_file


class FlightMissionData(APIView):

    def get(self, request, *args, **kwargs):

        status = 200

        try:
            mission = Mission.objects.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            mission = None
        
        if mission is None:
            result = "Mission with id '{0}' does not exist".format(kwargs['id'])
            status = 400
        else:
            points_qs = YDMissionPoint.objects.filter(mission__id=kwargs['id'])
            points_raw = json.loads(serializers.serialize('json', points_qs))
            at_create = ' '.join(str(mission.at_create).split('T'))[:-13]
            result = {'points':[],
                      'id': kwargs['id'],
                      'mission_name':mission.mission_name,
                      'description':mission.description,
                      'at_create':at_create, 
                      'user_info':mission.user_info}
            for point_raw in points_raw:
                fields = point_raw['fields']
                fields.pop('mission', None)
                result['points'].append(fields)

        return JsonResponse({'result':result}, status=status) 


class FlightMissionDataWithParams(APIView):
    def get(self, request, *args, **kwargs):
        status = 200

        mission_name = request.query_params.get('name', '')
        user = request.query_params.get('user', '')
        start_date = request.query_params.get('start_date', '1960-12-09T15:59:00.000Z')
        end_date = request.query_params.get('end_date', '2040-12-09T15:59:00.000Z')

        missions_qs = Mission.objects.filter(mission_name__icontains=mission_name,
                                               user_info__icontains=user,
                                               at_create__gte=start_date,
                                               at_create__lte=end_date)
        missions_raw = json.loads(serializers.serialize('json', missions_qs))
        missions = []
        for mission_raw in missions_raw:
            mission = mission_raw['fields']
            mission['id'] = mission_raw['pk']
            points_qs = YDMissionPoint.objects.filter(mission__id=mission['id'])
            points_raw = json.loads(serializers.serialize('json', points_qs))
            mission['points'] = []
            if len(points_raw) != 0:
                for point in points_raw:
                    point = point.get('fields')
                    point.pop('mission', None)
                    mission['points'].append(point)
            missions.append(mission)

        return JsonResponse({'result':missions}, status=status)  


class LoadFlightMissionData(APIView):
    
    parser_class = [JSONParser, FileUploadParser]
    
    def post(self, request):
        files = request.FILES
        data = json.loads(request.data['info'])

        status = 200
        message = 'Success'

        try:
            mission = Mission.objects.get(mission_name=data['mission_name'])
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

        new_mission = Mission()
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
        missions = Mission.objects.all()
        data = json.loads(serializers.serialize('json', missions, fields=('mission_name','user_info','at_create')))
        response = {'result': []}
        for mission in data:
            fields = mission['fields']
            fields['at_create'] = ' '.join(fields['at_create'].split('T'))[:-5]
            log_count = LogFile.objects.filter(mission__id=mission['pk']).count()
            fields['log_count'] = log_count
            fields['id'] = mission['pk']
            response['result'].append(fields)
        return JsonResponse(response, status=200)


class LoadMissionLog(APIView):
    
    def post(self, request):
        files = request.FILES
        data = json.loads(request.data['info'])

        status = 200
        message = 'Success'

        try:
            mission = Mission.objects.get(mission_name=data['mission_name'])
        except ObjectDoesNotExist:
            mission = None

        if mission is None and data['mission_name']!='':
            status = 400
            message = "Миссия с названием '{0}' не существует. Для сохранения файла лога без миссии оставьте поле 'имя миссии' пустым".format(data['mission_name'])
        else:
            new_log = LogFile()
            file_name = uuid.uuid4().hex +'.'+ files['log'].name.split('.')[1]
            files['log'].name = file_name

            new_log.mission = mission
            new_log.flight_data = data['flight_data']
            new_log.description = data['mission_description']
            new_log.at_create = timezone.now()
            new_log.upload = files['log']
            new_log.save()

        return JsonResponse({'message':message}, status=status) 


class MissionLogDataWithParams(APIView):

    def get(self, request):
        status = 200

        mission_name = request.query_params.get('name', '')
        start_date = request.query_params.get('start_date', '1960-12-09T15:59:00.000Z')
        end_date = request.query_params.get('end_date', '2040-12-09T15:59:00.000Z')

        try:
            mission_qs = Mission.objects.get(mission_name__icontains=mission_name)
        except:
            mission_qs = None

        if mission_qs is None or mission_name=='':
            logs_qs = LogFile.objects.filter(at_create__gte=start_date,
                                                at_create__lte=end_date)
        else:
            logs_qs = LogFile.objects.filter(mission=mission_qs,
                                                at_create__gte=start_date,
                                                at_create__lte=end_date)
    
        logs_raw = json.loads(serializers.serialize('json', logs_qs))
        logs = []

        for log_raw in logs_raw:
            log = log_raw['fields']
            if not log['mission'] is None:
                mission = Mission.objects.get(id=log['mission'])
                log['mission'] = mission.mission_name
            points = read_log_bin_file(MEDIA_ROOT+'/'+log['upload'])
            log['points'] = points
            logs.append(log)

        return JsonResponse({'result':logs}, status=status)  