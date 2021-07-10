from django.contrib import admin
import openpyxl
from bazdidkhodro.models import (Image,Insurer,Visit,Document)
from django.utils.safestring import mark_safe
from django import forms
import csv
from django.contrib import messages
from django.forms import ValidationError

class ImageAdmin(admin.ModelAdmin):
    model = Image
    fields = ['']
    list_display = ['get_img','get_visit_info']
    list_per_page = 10

    def get_img(self,obj):
        if len(str(obj.img)) > 0:
            return mark_safe(f'<img src="/media/{obj.img}" width="60" height="60" />')
    get_img.short_description = "تصویر"

    def get_visit_info(self,obj):
        visit = Visit.objects.get(pk=obj.visit_id)
        return visit.insurer

class ImageInline(admin.TabularInline):
    model = Image
    exclude = ['display_img','delete_item']
    readonly_fields = ['display_img','delete_item']
    extra = 0

    def delete_item(self,obj):
        if len(str(obj.img)) > 0:
            return mark_safe(f'<a class="deletelink" href="/admin/{self.model._meta.app_label}/{self.model.__name__.lower()}/{obj.id}/delete/"></a>')

    delete_item.short_description = "حذف"
    def display_img(self,obj):
        if len(str(obj.img)) > 0:
            return mark_safe(f'<img src="/media/{obj.img}" width="80" height="80" />')
        else:
            return ""
    display_img.short_description = "تصویر اصلی"


class VisitAdmin(admin.ModelAdmin):
    model = Visit
    fields = ['insurer', 'year','finished']
    search_fields = ('insurer','year','finished')
    list_filter = ('finished',)
    list_display = ('insurer', 'visitor', 'year','finished')
    inlines = [ImageInline]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.user.groups.filter(name='employee').exists():
            if change == False:
                obj.visitor = request.user
            super().save_model(request,obj,form,change)


class InsurerForm(forms.ModelForm):
    csv_file = forms.FileField(required=False,label="فایل اکسل")
    field_name = forms.CharField(max_length=5,required=False,label="ستون فیلد نام")
    field_mobile = forms.CharField(max_length=5,required=False,label="ستون فیلد تلفن همراه")
    field_address = forms.CharField(max_length=5,required=False,label="ستون فیلد آدرس")

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if len(str(mobile)) >= 10 or mobile is None:
            return mobile
        else:
            raise ValidationError("شماره موبایل را صحیح وارد کنید")

    class Meta:
        model = Insurer
        fields = '__all__'


class InsurerAdmin(admin.ModelAdmin):
    model = Insurer
    list_display = ['name','mobile','pelak','created_by']
    fieldsets = (
        ('تکی',{'fields':['name','mobile','address','p1','p2','p3','p4']}),
        ('گروهی',{'fields':('csv_file','field_name','field_mobile','field_address')})
        )
    form = InsurerForm

    def decode_utf8(self,input_iterator):
        for l in input_iterator:
            yield l.decode('utf-8')

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser or request.user.groups.filter(name="employee").exists():
            if "csv_file" in request.FILES and  len(str(request.FILES['csv_file'])) > 0:
                #csv_file = request.FILES['csv_file']
                #reader = csv.DictReader(self.decode_utf8(csv_file))
                field_name = request.POST["field_name"]
                field_mobile = request.POST["field_mobile"]
                field_address = request.POST["field_address"]
                excel_file = request.FILES['csv_file']
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb["Sheet1"]
                data_list = list()
                mobiles_list = list()
                for i,row in enumerate(worksheet.iter_rows()):
                    if i==0:
                        continue
                    row_data = dict()
                    row_data['created_by'] = request.user
                    for j,cell in enumerate(row):
                        if len(field_name) > 0 and j==int(field_name):
                            row_data['name'] = str(cell.value)
                        elif len(field_mobile) > 0 and j==int(field_mobile):
                            mob = "0" + str(cell.value)[-10:]
                            mobiles_list.append(mob)
                            row_data['mobile'] = mob
                        elif len(field_address) > 0 and j == int(field_address):
                            row_data['address'] = str(cell.value)
                    data_list.append(row_data)
                c = len(Insurer.objects.filter(mobile__in=mobiles_list))
                obj_list = [Insurer(**data_dict) for data_dict in data_list]
                objs = Insurer.objects.bulk_create(obj_list,ignore_conflicts=True)
                if c==0:
                    messages.success(request,f"تمام اطلاعات با موفقیت ثبت شد.تعداد : {objs.__len__()}")
                else:
                    messages.success(request,f"تعداد کاربران درج شده {objs.__len__() - c} و کاربران تکرای { c}")
            else:
                if len(obj.name) >0 and len(obj.mobile) >0:
                    if not change:
                        obj.created_by = request.user
                    obj.mobile = "0" + str(obj.mobile)[-10:]
                    obj.pelak = str(obj.p1)+"-"+str(obj.p2)+"-"+str(obj.p3)+"-"+str(obj.p4)
                    super().save_model(request,obj,form,change)
                    messages.success(request,"بیمه گذار با موفقیت ذخیره شد")
                else:
                    messages.error(request, "نام و شماره تلفن نمیتواند خالی باشد")

    def message_user(self, request, message, level=messages.INFO, extra_tags='',fail_silently=False):
        pass


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    fields = [
        'user',
        'file',
    ]
    list_display = [
        'user',
        'file',
    ]


admin.site.register(Visit, VisitAdmin)
admin.site.register(Insurer,InsurerAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Document,DocumentAdmin)

