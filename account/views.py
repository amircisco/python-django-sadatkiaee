from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from bazdidkhodro.models import (Image, Insurer, Visit)
import traceback
from account.models import Family as Group
from django.shortcuts import redirect
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.state import token_backend
from account.models import User


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.is_superuser:
            grps = ['superuser']
        else:
            grps = [x[1] for x in list(self.user.groups.values_list())]
        data['groups'] = grps
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_id=decoded_payload['user_id']
        current_user = User.objects.get(id=user_id)
        if current_user.is_superuser:
            grps = ['superuser']
        else:
            grps = [x[1] for x in list(current_user.groups.values_list()) ]
        data['groups'] = grps
        return data


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainLifetimeSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshLifetimeSerializer


def home_to_admin(request):
    return redirect('/admin')


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
