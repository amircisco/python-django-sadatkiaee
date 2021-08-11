import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from timesheet.models import TimeSheet,AccessPoint
import jdatetime
from .serializers import GetTimeSheetSerializer, EnterTimeSheetSerializer, ExitTimeSheetSerializer
from rest_framework.response import Response
from rest_framework import status


class GetSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTimeSheetSerializer

    def post(self, request, *args, **kwargs):
        ssid = request.data['ssid']
        bssid = request.data['bssid']
        if AccessPoint.objects.filter(ssid=ssid,bssid=bssid.upper()).exists() or AccessPoint.objects.filter(ssid=ssid,bssid=bssid.lower()).exists():
            current_date = jdatetime.datetime.now().date()
            timesheet = TimeSheet.objects.filter(current_date=str(current_date), user_id=request.user.id ).first()
            if timesheet is not None:
                if len(str(timesheet.exit_time)) == 0:
                    serializer = GetTimeSheetSerializer(instance=timesheet)
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
                elif len(str(timesheet.exit_time)) > 0:
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_202_ACCEPTED,data={"current_date":str(current_date)})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EnterTimeSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnterTimeSheetSerializer

    def post(self, request, *args, **kwargs):
        current_date = str(jdatetime.datetime.now().date())
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
        current_date = jdatetime.datetime.now().date()
        exit_time = str(jdatetime.datetime.now().time()).split(".")[0]
        timesheet = TimeSheet.objects.get(current_date=str(current_date), user=request.user)
        data_serializer = {"exit_time":exit_time}
        serializer = ExitTimeSheetSerializer(instance=timesheet, partial=True, data=data_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)