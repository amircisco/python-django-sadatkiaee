from django.contrib.auth.forms import forms
from bazdidkhodro.models import (Visit)


class VisitCreateForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('insurer', 'year')
