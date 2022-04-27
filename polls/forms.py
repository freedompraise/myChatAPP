from django.forms import ModelForm
from .models import Room
from django.forms import forms

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



