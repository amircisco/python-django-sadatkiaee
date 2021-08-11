from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from timesheet.models import TimeSheet,AccessPoint
import jdatetime
from .serializers import GetTimeSheetSerializer,EnterTimeSheetSerializer,ExitTimeSheetSerializer
from rest_framework.response import Response
from rest_framework import status


class GetSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetTimeSheetSerializer

    def get(self, request, *args, **kwargs):
        ssid = kwargs['ssid']
        bssid = kwargs['bssid']
        if AccessPoint.objects.filter(ssid=ssid,bssid=bssid).exists():
            current_date = jdatetime.datetime.now().date()
            timesheet = TimeSheet.objects.get(current_date=current_date, user = request.user )
            if timesheet is not None:
                serializer = GetTimeSheetSerializer(instance=timesheet)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EnterTimeSheetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnterTimeSheetSerializer

    def post(self, request, *args, **kwargs):
        current_date = jdatetime.datetime.now().date()
        enter_time = jdatetime.datetime.now().time()
        data_serializer = {"user":request.user, "current_date":current_date, "enter_time":enter_time}
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
        exit_time = jdatetime.datetime.now().time()
        timesheet = TimeSheet.objects.get(current_date=current_date, user=request.user)
        data_serializer = {"exit_time":exit_time}
        serializer = ExitTimeSheetSerializer(instance=timesheet, partial=True, data=data_serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)