from django.contrib import admin
from rest_framework import status

from timesheet.models import TimeSheet, AccessPoint


class TimeSheetAdmin(admin.ModelAdmin):
    model = TimeSheet
    fields = [
        'user',
        'current_date',
        'enter_time',
        'exit_time',
    ]
    list_display = [
        'user',
        'current_date',
    ]


class AccessPointAdmin(admin.ModelAdmin):
    model = AccessPoint
    fields = [
        'ssid',
        'bssid',
        'status',
    ]
    list_display = [
        'ssid',
        'status'
    ]
    status.boolean = True


admin.site.register(TimeSheet,TimeSheetAdmin)
admin.site.register(AccessPoint,AccessPointAdmin)