from django.contrib import admin
import openpyxl
from bazdidkhodro.models import (Image, Insurer, Visit, Document, DocumentFile, InsurerDocument, InsurerDocumentFile,
                                 MenuItems, MobileSignal)
from django.utils.safestring import mark_safe
from django import forms
from django.shortcuts import redirect,HttpResponseRedirect,reverse
from django.contrib import messages
from django.forms import ValidationError
from account.models import User


class ImageAdmin(admin.ModelAdmin):
    model = Image
    fields = [
        'visit',
    ]
    deleted_visit_id = None

    def has_module_permission(self, request):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        self.deleted_visit_id = Image.objects.get(id=object_id).visit_id
        return super(ImageAdmin, self).delete_view(request, object_id, extra_context)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_visit_change',args=(self.deleted_visit_id,)))


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


class DocumentFileAdmin(admin.ModelAdmin):
    model = DocumentFile
    deleted_document_id = None

    def has_module_permission(self, request):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        self.deleted_document_id = DocumentFile.objects.get(id=object_id).document_id
        return super(DocumentFileAdmin, self).delete_view(request, object_id, extra_context)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_document_change',args=(self.deleted_document_id,)))


class DocumentFileInline(admin.TabularInline):
    model = DocumentFile
    exclude = ['display_file','delete_item']
    readonly_fields = ['display_file','delete_item']
    extra = 0

    def delete_item(self,obj):
        if len(str(obj.file)) > 0:
            return mark_safe(f'<a class="deletelink" href="/admin/{self.model._meta.app_label}/{self.model.__name__.lower()}/{obj.id}/delete/"></a>')
    delete_item.short_description = "حذف"

    def display_file(self,obj):
        if len(str(obj.file)) > 0:
            return mark_safe(f'<img src="/media/{obj.file}" width="80" height="80" />')
        else:
            return ""
    display_file.short_description = "فایل اصلی"


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    fields = [
        'insurer',
    ]
    list_display = ['get_user_info','get_employee_info']
    list_per_page = 10
    inlines = [
        DocumentFileInline,
    ]

    def get_user_info(self,obj):
        insurer = Insurer.objects.get(pk=obj.insurer.id)
        return insurer
    get_user_info.short_description = "اطلاعات بیمه گذار"

    def get_employee_info(self,obj):
        employee = User.objects.get(pk=obj.employee.id)
        return employee
    get_employee_info.short_description = "کارمند ارسال کننده"


class InsurerDocumentFileAdmin(admin.ModelAdmin):
    model = InsurerDocumentFile
    deleted_document_id = None

    def has_module_permission(self, request):
        return False

    def delete_view(self, request, object_id, extra_context=None):
        self.deleted_document_id = InsurerDocumentFile.objects.get(id=object_id).document_id
        return super(InsurerDocumentFileAdmin, self).delete_view(request, object_id, extra_context)

    def response_delete(self, request, obj_display, obj_id):
        return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_insurerdocument_change',args=(self.deleted_document_id,)))


class InsurerDocumentFileInline(admin.TabularInline):
    model = InsurerDocumentFile
    exclude = ['display_file','delete_item']
    readonly_fields = ['display_file','delete_item']
    extra = 0

    def delete_item(self,obj):
        if len(str(obj.file)) > 0:
            return mark_safe(f'<a class="deletelink" href="/admin/{self.model._meta.app_label}/{self.model.__name__.lower()}/{obj.id}/delete/"></a>')
    delete_item.short_description = "حذف"

    def display_file(self,obj):
        if len(str(obj.file)) > 0:
            return mark_safe(f'<img src="/media/{obj.file}" width="80" height="80" />')
        else:
            return ""
    display_file.short_description = "فایل اصلی"


class InsurerDocumentAdmin(admin.ModelAdmin):
    model = InsurerDocument
    fields = [
        'user',
    ]
    list_display = ['get_user_info']
    list_per_page = 10
    inlines = [
        InsurerDocumentFileInline,
    ]

    def get_user_info(self,obj):
        insurer = Insurer.objects.get(pk=obj.user.id)
        return insurer
    get_user_info.short_description = "اطلاعات بیمه گذار"


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItems
    fields = ['name', 'link']
    list_display = ['name']


class MobileSignalAdmin(admin.ModelAdmin):
    model = MobileSignal
    list_display = ['menu', 'user', 'get_action', 'get_enter_date', 'get_leave_date', 'get_stay']
    list_per_page = 10
    search_fields = ['enter_date']
    list_filter = ["action","user__username"]

    def get_enter_date(self, obj):
        print(obj.enter_date)
        return str(obj.enter_date).split("+")[0]
    get_enter_date.short_description = "تاریخ ورود"

    def get_action(self,obj):
        ac = "ورود"
        if obj.action == "leave":
            ac = "خروج"
        return ac
    get_action.short_description = 'نوع'

    def get_leave_date(self,obj):
        is_online = "آنلاین"
        if obj.leave_date != None :
            is_online = obj.leave_date
        return is_online
    get_leave_date.short_description = "خروج"

    def get_stay(self,obj):
        stay = ""
        if obj.leave_date != None:
            stay = str(obj.leave_date - obj.enter_date).split('.')[0]
        return stay
    get_stay.short_description = "مدت ماندن"


admin.site.register(Visit, VisitAdmin)
admin.site.register(Insurer,InsurerAdmin)
admin.site.register(Image,ImageAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(DocumentFile,DocumentFileAdmin)
admin.site.register(InsurerDocument,InsurerDocumentAdmin)
admin.site.register(InsurerDocumentFile,InsurerDocumentFileAdmin)
admin.site.register(MenuItems,MenuItemAdmin)
admin.site.register(MobileSignal,MobileSignalAdmin)
