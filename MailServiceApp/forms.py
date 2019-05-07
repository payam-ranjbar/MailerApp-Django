from django import forms

from MailServiceApp.models import Mail


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())







