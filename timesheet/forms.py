from django import forms
from account.models import User
from django.db.models import Q
from .models import CommissionAmount, CommissionPercentage, SalarySetting


class CalcSalaryForm(forms.Form):
    ch = list(User.objects.filter(Q(groups__name="visitor") | Q(groups__name="employee")).values_list("id", "username"))
    ch.insert(0, ('0', 'انتخاب کارمند'))
    employee = forms.ChoiceField(label="کارمند", choices=ch)
    from_date = forms.DateField(label="از تاریخ")
    to_date = forms.DateField(label="تا تاریخ")

    def __init__(self):
        super().__init__()
        commissions_amount = CommissionAmount.objects.all()
        commission_percentage = CommissionPercentage.objects.all()
        salarysettings = SalarySetting.objects.first()
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

        self.fields["dinnertime"] = forms.CharField(label="زمان استراحت و ناهار",initial="30")
        self.fields["worktime"] = forms.CharField(label=salarysettings.verbose_name("worktime"), initial=salarysettings.worktime)
        self.fields["extraworktime"] = forms.CharField(label=salarysettings.verbose_name("extraworktime"), initial=salarysettings.extraworktime)
        self.fields["workamount"] = forms.CharField(label=salarysettings.verbose_name("workamount"), initial=salarysettings.workamount)
        self.fields["extraworkamount"] = forms.CharField(label=salarysettings.verbose_name("extraworkamount"), initial=salarysettings.extraworkamount)
