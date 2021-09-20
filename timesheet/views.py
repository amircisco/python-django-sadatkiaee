import extra as extra
from django.shortcuts import render
from django.http import HttpResponse
from .models import TimeSheet, SalarySetting
from django.db.models import F, Sum, ExpressionWrapper, fields,Func
from account.models import User


def calc_salary(request):
    employee = request.POST["employee"]
    employee_info = User.objects.get(id=employee)
    from_date = request.POST['from_date']
    to_date = request.POST['to_date']
    worktime = float(request.POST['worktime'])
    extraworktime = float(request.POST['extraworktime'])
    workamount = float(request.POST['workamount'])
    extraworkamount =float(request.POST['extraworkamount'])
    qs = TimeSheet.objects.filter(user=employee,current_date__range=(from_date,to_date))
    duration = ExpressionWrapper(F('exit_time') - F('enter_time'), output_field=fields.DurationField())
    all_work_timesheet = qs = qs.annotate(duration=duration)
    qs = qs.aggregate(sumwork=Sum('duration'))
    seconds = qs["sumwork"].total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours == worktime:
        amount = hours * workamount
        extraamount = int((((minutes * 100) / 60) * extraworkamount) / 100)
        last_work = int(amount + extraamount)
    elif hours > worktime:
        amount = worktime * workamount
        part1 = (hours - worktime) * extraworkamount
        part2 = int((((minutes * 100) / 60) * extraworkamount) / 100)
        extraamount = part1 + part2
        last_work = int(amount + extraamount)
    elif hours < worktime:
        part1 = hours * workamount
        part2 = int((((minutes * 100) / 60) * workamount) / 100)
        last_work = int(part1 + part2)

    list_commission_amount = []
    list_commission_percentage = []
    amount_set = set()
    percentage_set = set()
    for key in request.POST:
        if key.find("commission_amount") > -1:
            amount_set.add(int(''.join(filter(str.isdigit, key))))
        elif key.find("commission_percentage") > -1:
            percentage_set.add(int(''.join(filter(str.isdigit, key))))

    last_amount = 0
    for index in amount_set:
        commission_amount_name = request.POST[f"commission_amount_name_{index}"]
        commission_amount_amount = request.POST[f"commission_amount_amount_{index}"]
        commission_amount_count = request.POST[f"commission_amount_count_{index}"]
        cur = int(commission_amount_amount) * int(commission_amount_count)
        last_amount+=cur
        list_commission_amount.append({"name":commission_amount_name,"count":commission_amount_count,"amount":commission_amount_amount,"last":cur})

    last_percentage = 0
    for index in percentage_set:
        commission_percentage_name = request.POST[f"commission_percentage_name_{index}"]
        commission_percentage_percentage = request.POST[f"commission_percentage_percentage_{index}"]
        commission_percentage_sum = request.POST[f"commission_percentage_sum_{index}"]
        cur = int(float(commission_percentage_percentage) * int(commission_percentage_sum) / 100)
        last_percentage+=cur
        list_commission_percentage.append({"name": commission_percentage_name, "sum": commission_percentage_sum, "percentage": commission_percentage_percentage,"last": cur})

    return render(request,"timesheet/calc_salary.html",{
        "last_amount":last_amount,
        "last_percentage":last_percentage,
        "last_work":last_work,
        "majmoo": last_amount + last_percentage + last_work,
        "hours":hours,
        "minutes":minutes,
        "employee_name":employee_info.username,
        "employee_mobile": employee_info.mobile,
        "from_date":from_date,
        "to_date":to_date,
        "all_work_timesheet":all_work_timesheet,
        "list_commission_amount":list_commission_amount,
        "list_commission_percentage":list_commission_percentage,
    })