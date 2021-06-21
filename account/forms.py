from django import forms
from django.contrib.auth import forms as auth_forms
from account.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'mobile', 'password', 'groups', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return make_password(self.cleaned_data.get('password'))