from django import forms
from myapp.models import Document
from django.contrib.auth.models import User


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document 
        fields = {'descripcion','document','precio'}

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='Crear como administrador', required=False)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
