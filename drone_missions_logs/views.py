from xxlimited import new
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from braces.views import CsrfExemptMixin


import json
import uuid

from drone_info.settings import MEDIA_ROOT
from drone_missions_logs.models import Mission, LogFile, YDMissionPoint, MavLinkPX4MissionPoint,PROTOCOL_TYPE_CHOICES
from drone_missions_logs.log_mission_parsers import parse_yd_mission_bytes_array, parse_yd_log_bin_file,\
                                                    parse_mavlink_mission_waypoint, parse_mavlink_log_bin_file


class MissionView(APIView): # get mission with points by id

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
            if mission.protocol_type == 'YD':
                points_qs = YDMissionPoint.objects.filter(mission__id=mission.id)
            else:
                points_qs = MavLinkPX4MissionPoint.objects.filter(mission__id=mission.id) 
            # points_qs = YDMissionPoint.objects.filter(mission__id=kwargs['id'])
            points_raw = json.loads(serializers.serialize('json', points_qs))
            at_create = ' '.join(str(mission.at_create).split('T'))[:-13]
            result = {'points':[],
                      'id': kwargs['id'],
                      'mission_name':mission.mission_name,
                      'description':mission.description,
                      'at_create':at_create,
                      'protocol_type':mission.protocol_type, 
                      'user_info':mission.user_info}
            for point_raw in points_raw:
                fields = point_raw['fields']
                fields.pop('mission', None)
                result['points'].append(fields)

        return JsonResponse({'result':result}, status=status) 


class MissionViewWithParams(APIView): # get missions set by params
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
            if mission['protocol_type'] == 'YD':
                points_qs = YDMissionPoint.objects.filter(mission__id=mission['id'])
            else:
                points_qs = MavLinkPX4MissionPoint.objects.filter(mission__id=mission['id']) 
            points_raw = json.loads(serializers.serialize('json', points_qs))
            mission['points'] = []
            if len(points_raw) != 0:
                for point in points_raw:
                    point = point.get('fields')
                    point.pop('mission', None)
                    mission['points'].append(point)
            missions.append(mission)

        return JsonResponse({'result':missions}, status=status)  


class MissionDataLoad(CsrfExemptMixin, APIView): #save mission to db with points
    
    parser_class = [JSONParser, FileUploadParser]
    authentication_classes = []
    
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
            if self._check_protocol_valid(data['protocol_type']):
                new_mission = self._createMission(data, files)
                self._createMissionPoints(files['mission'], new_mission)
            else:
                message = "Pritocol type unknown"
                status = 400
            
        else:
            status = 400
            message = 'Mission with same name already exist'

        return JsonResponse({'message':message}, status=status)

    def _check_protocol_valid(slef, protocol):
        for valid_protocol in PROTOCOL_TYPE_CHOICES:
            if valid_protocol[0] == protocol:
                return True
        return False

    def _createMission(self, data, files):
        file_name = uuid.uuid4().hex +'.'+ files['mission'].name.split('.')[1]
        files['mission'].name = file_name

        new_mission = Mission()
        new_mission.mission_name = data['mission_name']
        new_mission.user_info = data['author']
        new_mission.description = data['mission_description']
        new_mission.protocol_type = data['protocol_type']
        new_mission.flight_mission_file = files['mission']
        new_mission.at_create = timezone.now()
        new_mission.save()
        return new_mission
    
    def _createMissionPoints(self, file, mission):
        if mission.protocol_type == 'YD':
            file.file.seek(0)
            bytes_array = file.file.read()
            points = parse_yd_mission_bytes_array(bytes_array)
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
        
        if mission.protocol_type == 'ML' or mission.protocol_type == 'PX4':
            file.file.seek(0)
            points = []
            if file.name.endswith('.waypoints'):
                points = parse_mavlink_mission_waypoint(file.file)

            for point in points:
                new_point = MavLinkPX4MissionPoint()
                new_point.mission = mission
                new_point.seq = point[0]
                new_point.current = point[1]
                new_point.frame = point[2]
                new_point.command = point[3]
                
                new_point.param1 = point[4]
                new_point.param2 = point[5]
                new_point.param3 = point[6]
                new_point.param4 = point[7]
                
                new_point.x = point[8]
                new_point.y = point[9]
                new_point.z = point[10]
                new_point.autocontinue = point[11]
                new_point.target_component = 0
                new_point.save()                


class MissionViewAll(APIView): #get all missions without points
    
    def get(self, request):
        missions = Mission.objects.all()
        data = json.loads(serializers.serialize('json', missions, fields=('mission_name','user_info','at_create','protocol_type')))
        response = {'result': []}
        for mission in data:
            fields = mission['fields']
            fields['at_create'] = ' '.join(fields['at_create'].split('T'))[:-5]
            log_count = LogFile.objects.filter(mission__id=mission['pk']).count()
            fields['log_count'] = log_count
            fields['id'] = mission['pk']
            response['result'].append(fields)
        return JsonResponse(response, status=200)


class LogDataLoad(CsrfExemptMixin, APIView): #save log file to bd
    authentication_classes = []


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
            new_log.protocol_type = data['protocol_type']
            new_log.upload = files['log']
            new_log.save()

        return JsonResponse({'message':message}, status=status) 


class LogViewWithParams(APIView): #get log with points by params

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
                
            if log['protocol_type'] == 'YD':
                points = parse_yd_log_bin_file(MEDIA_ROOT+'/'+log['upload'])
                
            elif log['protocol_type'] == 'PX4' or log['protocol_type'] == 'ML':
                points = parse_mavlink_log_bin_file(MEDIA_ROOT+'/'+log['upload'])
            
            else:
                points = []
            log['points'] = points
            logs.append(log)

        return JsonResponse({'result':logs}, status=status)  