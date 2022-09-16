from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.urls import URLPattern
from .models import Cluster, Todo, Nutzer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

        
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'deadline', 'percent')

        
class ClusterForm(ModelForm):
    class Meta:
        model = Cluster
        fields = ('title', 'quantity', 'duration', 'availability')

class RegisterForm(UserCreationForm):
#	matrikelnummer = forms.IntegerField(max_value="1000000")

	class Meta:
		model = User
		fields = ("username", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		#user.matrikelnummer = self.cleaned_data['matrikelnummer']
		if commit:
			user.save()
		return user
