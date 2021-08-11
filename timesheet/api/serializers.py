from pyexpat import model

from timesheet.models import TimeSheet
from rest_framework import serializers


class GetTimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = [
            'user',
            'current_date',
            'enter_time',
        ]


class EnterTimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = [
            'user',
            'current_date',
            'enter_time',
        ]


class ExitTimeSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSheet
        fields = [
            'user',
            'current_date',
            'exit_time',
        ]