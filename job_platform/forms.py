from django import forms
from core.models import Application
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        # Add CSS classes to fields
        self.fields["username"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Password"}
        )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Add CSS classes to fields
        self.fields["username"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Confirm Password"}
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        # Add CSS classes to fields
        self.fields["username"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Username"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Email"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Your First Name"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "main-input", "placeholder": "Enter Your Last Name"}
        )


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status"]
        widgets = {
            "status": forms.Select(),
        }
