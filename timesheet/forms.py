import datetime
from django import forms
from account.models import User
from django.db.models import Q
from .models import CommissionAmount, CommissionPercentage,TimeSheet


class TimesheetForm(forms.ModelForm):
    current_date = forms.CharField(label="تاریخ",)
    class Meta:
        model = TimeSheet
        fields = [
            'user',
            'current_date',
            'enter_time',
            'exit_time',
        ]

    def clean_current_date(self):
        return TimeSheet.gcurrent_date(self.cleaned_data['current_date'])


class CalcSalaryForm(forms.Form):
    from_date = forms.DateField(label="از تاریخ")
    to_date = forms.DateField(label="تا تاریخ")

    def __init__(self):
        super().__init__()
        ch = list(User.objects.filter(Q(groups__name="visitor") | Q(groups__name="employee")).values_list("id", "username"))
        ch.insert(0, ('0', 'انتخاب کارمند'))
        self.fields["employee"] = forms.ChoiceField(label="کارمند", choices=ch)
        commissions_amount = CommissionAmount.objects.all()
        commission_percentage = CommissionPercentage.objects.all()
        for index, item in enumerate(commissions_amount,start=1):
            self.fields[f"commission_amount_name_{index}"] = forms.CharField(label=item.name, initial=item.name)
            self.fields[f"commission_amount_name_{index}"].widget.attrs['readonly'] = True
            self.fields[f"commission_amount_amount_{index}"] = forms.CharField(label="مبلغ پورسانت", initial=item.amount)
            self.fields[f"commission_amount_count_{index}"] = forms.IntegerField(label="تعداد", initial=0,widget=forms.TextInput(attrs={'class': 'rowfield'}))
        for index, item in enumerate(commission_percentage,start=1):
            self.fields[f"commission_percentage_name_{index}"] = forms.CharField(label=item.name, initial=item.name)
            self.fields[f"commission_percentage_name_{index}"].widget.attrs['readonly'] = True
            self.fields[f"commission_percentage_percentage_{index}"] = forms.CharField(label="درصد پورسانت", initial=item.percentage)
            self.fields[f"commission_percentage_sum_{index}"] = forms.IntegerField(label="مجموع", initial=0,widget=forms.TextInput(attrs={'class': 'rowfield'}))

        self.fields["tamin"] = forms.CharField(label="بیمه تامین اجتماعی", initial="2650000")
        self.fields["bon"] = forms.CharField(label="بن نقدی", initial="600000")
        self.fields["maskan"] = forms.CharField(label="حق مسکن", initial="450000")
        self.fields["payeh"] = forms.CharField(label="پایه حقوق", initial="26550000")
        self.fields["dinnertime"] = forms.CharField(label="زمان استراحت و ناهار",initial="30")
        self.fields["worktime"] = forms.CharField(label="ساعت کاری", initial="176")
        self.fields["extraworktime"] = forms.CharField(label="ساعت اضافه کاری", initial="120")
        self.fields["workamount"] = forms.CharField(label="دستمزد یک ساعت کاری", initial="80000")
        self.fields["extraworkamount"] = forms.CharField(label="دستمزد یک ساعت اضافه کاری", initial="170000")