from django import forms
from django.contrib.auth import get_user_model
from app_accounting.models import Social

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'avatar', 'email', 'about')
        # exclude = ('password', 'last_login')


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        exclude = ('user', )