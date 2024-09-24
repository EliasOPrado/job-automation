from django import forms
from core.models import Application
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Add CSS classes to fields
        self.fields['username'].widget.attrs.update({'class': 'main-input', 'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'class': 'main-input', 'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'class': 'main-input', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget.attrs.update({'class': 'main-input', 'placeholder': 'Confirm Password'})



class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(),
        }
