from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile
from users.models import Profile, Group


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    fname = forms.TextInput()
    lname = forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    fname = forms.TextInput()
    lname = forms.TextInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class GroupUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['image']