from django.forms import ModelForm
from .models import Room,User
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=[
'host','participants'
        ]

class InputMessage(forms.Form):
    class Meta:
        model=Room
        fields='__body__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields= ['name','username','email','bio','avatar']

class myUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username','email','password1']

