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


