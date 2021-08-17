from django.contrib import admin
from rest_framework import status
from django.http import HttpResponse
from timesheet.models import TimeSheet, AccessPoint
import csv
import datetime


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
        'get_current_date',
        'enter_time',
        'exit_time',
    ]

    def get_current_date(self, obj):
        arr_cur = str(obj.current_date).split("-")
        return arr_cur[0]+"-"+arr_cur[1]+"-"+arr_cur[2]
    get_current_date.short_description = "تاریخ"


def calc_majmoo(exit_time, enter_time):
    if exit_time is None or  enter_time is None:
        return ""
    dateTimeA = datetime.datetime.combine(datetime.date.today(), exit_time)
    dateTimeB = datetime.datetime.combine(datetime.date.today(), enter_time)
    dateTimeDifference = dateTimeA - dateTimeB
    dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
    arr_majmoo = str(dateTimeDifferenceInHours).split(".")
    majmoo = arr_majmoo[0] + "." + arr_majmoo[1][:2]
    return majmoo


class TimeSheetProxy(TimeSheet):
    class Meta:
        proxy = True
        verbose_name = "گزارش ورود خروج کارمند"
        verbose_name_plural = "گزارش ورود خروج کارمندان"


class TimeSheetAdminReport(admin.ModelAdmin):
    model = TimeSheetProxy
    list_display = [
        'user',
        'get_current_date',
        'enter_time',
        'exit_time',
        'majmoo',
    ]
    search_fields = ['current_date']
    list_filter = ['user__username']
    actions = ['export_csv']

    def majmoo(self,obj):
        return calc_majmoo(obj.exit_time, obj.enter_time)
    majmoo.short_description = "مجموع ساعت"

    def get_queryset(self, request):
        qs = super(TimeSheetAdminReport, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return TimeSheet.objects.filter(user=request.user)

    def get_current_date(self, obj):
        arr_cur = str(obj.current_date).split("-")
        return arr_cur[0]+"-"+arr_cur[1]+"-"+arr_cur[2]
    get_current_date.short_description = "تاریخ"

    def export_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')
        response['Content-disposition'] = 'attachment; filename="timesheet.csv"'
        writer = csv.writer(response)
        writer.writerow(['نام کارمند', 'تاریخ', 'ساعت ورود', 'ساعت خروج', 'مجموع'])
        books = queryset.values_list('user__username', 'current_date', 'enter_time', 'exit_time')
        for book in books:
            majmoo = calc_majmoo(book[3],book[2])
            new_book = book + (majmoo,)
            writer.writerow(new_book)
        return response

    export_csv.short_description = "خروجی اکسل"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AccessPointAdmin(admin.ModelAdmin):
    model = AccessPoint
    fields = [
        'ssid',
        'bssid',
        'ip',
        'subnet',
        'status',
    ]
    list_display = [
        'ssid',
        'status'
    ]
    status.boolean = True


admin.site.register(TimeSheet, TimeSheetAdmin)
admin.site.register(TimeSheetProxy, TimeSheetAdminReport)
admin.site.register(AccessPoint, AccessPointAdmin)