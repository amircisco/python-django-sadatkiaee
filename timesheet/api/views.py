import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from timesheet.models import TimeSheet,AccessPoint
import jdatetime
from .serializers import GetTimeSheetSerializer, EnterTimeSheetSerializer, ExitTimeSheetSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings as config_setting
import datetime


class GetSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTimeSheetSerializer

    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request, *args, **kwargs):
        details = request.data['details']
        if "ssid" in details and str(details["ssid"]).__len__() == 0:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        edame = False
        if details["bssid"] == "02:00:00:00:00:00":
            arr_ip = details["ipAddress"].split(".")
            ip = arr_ip[0]+"."+arr_ip[1]+"."+arr_ip[2]+".1"
            if config_setting.ACCESSPOINT_IP_CHECK:
                client_ip = self.get_client_ip(request)
                if AccessPoint.objects.filter(ip=ip,subnet=details["subnet"]).exists() and config_setting.ACCESSPOINT_IP in client_ip:
                    edame = True
            else:
                if AccessPoint.objects.filter(ip=ip,subnet=details["subnet"]).exists():
                    edame = True
        else:
            if AccessPoint.objects.filter(ssid=details["ssid"],bssid=details["bssid"].upper()).exists() or AccessPoint.objects.filter(ssid=details["ssid"],bssid=details["bssid"].lower()).exists():
                edame = True

        if edame == True:
            current_date = datetime.datetime.now().date()
            timesheet = TimeSheet.objects.filter(current_date=str(current_date), user_id=request.user.id).first()
            if timesheet is not None:
                if timesheet.exit_time is None:
                    serializer = GetTimeSheetSerializer(instance=timesheet)
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
                elif timesheet.exit_time is not None:
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_202_ACCEPTED, data={"current_date": str(current_date)})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EnterTimeSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnterTimeSheetSerializer

    def post(self, request, *args, **kwargs):
        current_date = str(datetime.datetime.now().date())
        enter_time = str(jdatetime.datetime.now().time()).split(".")[0]
        data_serializer = {"user":request.user.id, "current_date":current_date, "enter_time":enter_time}
        serializer = EnterTimeSheetSerializer(data=data_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ExitTimeSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExitTimeSheetSerializer

    def post(self, request, *args, **kwargs):
        current_date = datetime.datetime.now().date()
        exit_time = str(jdatetime.datetime.now().time()).split(".")[0]
        timesheet = TimeSheet.objects.get(current_date=str(current_date), user=request.user)
        data_serializer = {"exit_time":exit_time}
        serializer = ExitTimeSheetSerializer(instance=timesheet, partial=True, data=data_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)