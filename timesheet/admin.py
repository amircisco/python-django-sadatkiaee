import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import status
from timesheet.models import TimeSheet, AccessPoint, CommissionAmount, CommissionPercentage
from .forms import CalcSalaryForm,TimesheetForm


class TimeSheetAdmin(admin.ModelAdmin):
    model = TimeSheet
    form = TimesheetForm
    list_display = [
        'user',
        'get_current_date',
        'enter_time',
        'exit_time',
    ]

    def get_current_date(self, obj):
        return obj.jcurrent_date(obj.current_date)

    get_current_date.short_description = "تاریخ"


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


class CommissionAmountAdmin(admin.ModelAdmin):
    model = CommissionAmount
    fields = [
        'name',
        'amount',
    ]
    list_display = [
        'name',
        'get_value',
    ]

    def get_value(self, obj):
        return str(obj.commaamount) + " ریال"

    get_value.short_description = "مقدار"


class CommissionPercentageAdmin(admin.ModelAdmin):
    model = CommissionPercentage
    fields = [
        'name',
        'percentage',
    ]
    list_display = [
        'name',
        'get_value',
    ]

    def get_value(self, obj):
        return str(obj.percentage) + "%"

    get_value.short_description = "مقدار"


class CalcSalaryTimeSheetProxy(TimeSheet):
    class Meta:
        proxy = True
        verbose_name = "محاسبه حقوق و دستمزد"
        verbose_name_plural = "محاسبه حقوق و دستمزد"


class CalcSalaryTimeSheetAdmin(admin.ModelAdmin):
    model = CalcSalaryTimeSheetProxy

    def get_urls(self):
        form = CalcSalaryForm
        return [
            path('calc_salary_changelist/', TemplateView.as_view(template_name="admin/calc_salary_changelist.html"),
                 {"page_title":"محاسبه حقوق و دستمزد", "form":form},
                 name='{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)),
            path('calc_salary_add/', TemplateView.as_view(template_name="admin/calc_salary_changelist.html"),
                 {"page_title":"محاسبه حقوق و دستمزد", "form":form},
                 name='{}_{}_add'.format(
                     self.model._meta.app_label, self.model._meta.model_name)),
        ]


admin.site.register(CalcSalaryTimeSheetProxy, CalcSalaryTimeSheetAdmin)
admin.site.register(CommissionAmount, CommissionAmountAdmin)
admin.site.register(CommissionPercentage, CommissionPercentageAdmin)
admin.site.register(TimeSheet, TimeSheetAdmin)
admin.site.register(AccessPoint, AccessPointAdmin)