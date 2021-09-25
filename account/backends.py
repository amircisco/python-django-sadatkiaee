from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from account.models import User


class EmailModelBackend(ModelBackend):
    """
    authentication class to login with the email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username == None:
            username = kwargs.get('mobile')
        if len(username)==11 and username.isdigit():
            user = User.objects.filter(mobile=username).first()
            if user is not None and user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

