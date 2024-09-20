from django import forms
from core.models import Application

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(),
        }
