from django import forms
from core.models import Application
from django.contrib.auth.models import User


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(),
        }

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id']
