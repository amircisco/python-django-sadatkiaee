from django.contrib import admin
from account.models import User
from account.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from account.models import Family
from django.contrib.auth.models import Group
from django.db.models import Q

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['mobile', 'username', 'groups', 'password', 'is_active', 'is_staff', 'is_superuser', 'email', ]
    list_display = ['username', 'mobile', 'level', ]
    form = UserChangeForm
    add_form = UserCreationForm

    def level(self, obj):
        d = {'visitor': 'بازدید کننده', 'employee': 'کارمند'}
        if obj.groups.filter(Q(name='visitor') | Q(name="employee")).exists():
            return  d.get(list(obj.groups.filter(Q(name='visitor') | Q(name="employee")))[0].name)
        return "مدیرکل"
    level.short_description = "سطح کاربری"


class FamilyAdmin(admin.ModelAdmin):
    model = Family
    fields = ['name', 'permissions']
    list_display = ['get_name']

    def get_name(self,obj):
        return obj.get_name_group(obj.name)
    get_name.short_description = "گروه کاربری"


admin.site.register(Family,FamilyAdmin)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)