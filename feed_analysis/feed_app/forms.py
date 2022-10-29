from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import PasswordInput


# Create your forms here.

class loginform(forms.Form):
	uname = forms.CharField(label="uname", max_length=25)
	password = forms.CharField(widget=PasswordInput)