from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from bazdidkhodro.models import (Image, Insurer, Visit)
import traceback
from account.models import Family as Group


def install(request):
    if request.user.is_superuser:
        try:
            per_view_image = Permission.objects.get(codename='view_image')
            per_add_image = Permission.objects.get(codename='add_image')
            per_change_image = Permission.objects.get(codename='change_image')
            per_delete_image = Permission.objects.get(codename='delete_image')

            per_view_insurer = Permission.objects.get(codename='view_insurer')
            per_add_insurer = Permission.objects.get(codename='add_insurer')
            per_change_insurer = Permission.objects.get(codename='change_insurer')
            per_delete_insurer = Permission.objects.get(codename='delete_insurer')

            per_view_visit = Permission.objects.get(codename='view_visit')
            per_add_visit = Permission.objects.get(codename='add_visit')
            per_change_visit = Permission.objects.get(codename='change_visit')
            per_delete_visit = Permission.objects.get(codename='delete_visit')

            gr_visitor = Group.objects.create(name='visitor')
            gr_employee = Group.objects.create(name='employee')

            gr_visitor.permissions.add(per_view_image)
            gr_visitor.permissions.add(per_add_image)
            gr_visitor.permissions.add(per_view_insurer)
            gr_visitor.permissions.add(per_add_insurer)
            gr_visitor.permissions.add(per_view_visit)
            gr_visitor.permissions.add(per_add_visit)

            gr_employee.permissions.add(per_view_image)
            gr_employee.permissions.add(per_add_image)
            gr_employee.permissions.add(per_change_image)
            gr_employee.permissions.add(per_view_insurer)
            gr_employee.permissions.add(per_add_insurer)
            gr_employee.permissions.add(per_change_insurer)
            gr_employee.permissions.add(per_view_visit)
            gr_employee.permissions.add(per_add_visit)
            gr_employee.permissions.add(per_change_visit)

            gr_employee.save()
            gr_visitor.save()
            print(gr_employee)
            return HttpResponse("<h1>install finish</h1>")
        except:
            traceback.print_exc()
            return HttpResponse("<h1>before installed</h1>")

    return HttpResponse("<h1>Access Denied</h1>")
