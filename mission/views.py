from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FileUploadParser
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from mission.models import Mission, Point, UserInfo

class TestApi(APIView):

    parser_class = [JSONParser, FileUploadParser]

    def post(self, request):
        files = request.FILES
        data = request.data
        mission = None

        if not files.get('file', None) is None:
            # with files['file'] as f:
            #     firstline = f.readline()
            return JsonResponse({"Error":"This function not aviable"}, status=400)

        try:
            mission = Mission.objects.get(mission_name=data['mission_name'],at_create=data['mission_create_datetime'])
        except ObjectDoesNotExist:
            print('Mission does not exist')

        if mission is None:
            mission = Mission(mission_name=data.get('mission_name'),
                                  at_create=data.get('mission_create_datetime'))
            try:
                user_info = UserInfo.objects.get(system_user_name=data['mission_system_user_name'],
                                                 ip_address=data['mission_ip_address'],
                                                 operation_system=data['mission_operation_system'],
                                                 ardupilot_version=data['mission_ardupilot_version'])
            except ObjectDoesNotExist:
                user_info = None
            
            if user_info is None:
                user_info = UserInfo(system_user_name=data['mission_system_user_name'],
                                     ip_address=data['mission_ip_address'],
                                     operation_system=data['mission_operation_system'],
                                     ardupilot_version=data['mission_ardupilot_version'])
                user_info.save()
            
            mission.user_info = user_info
            mission.save()
    
        self._newPointFromData(data, mission)

        return JsonResponse({}, status=200)
    
    def get(self, request):
        return JsonResponse({}, status=200)

    def _newPointFromData(self, data, mission):
        new_point = Point(param1=data['param1'], param2=data['param2'], param3=data['param3'],
                            param4=data['param4'], x=data['x'], y=data['y'], z=data['z'],
                            seq=data['seq'], command=data['command'], target_system=data['target_system'],
                            target_component=data['target_component'], frame=data['frame'],
                            current=data['current'], autocontinue=data['autocontinue'], mission_type=data['mission_type'])
        new_point.mission = mission
        new_point.save()