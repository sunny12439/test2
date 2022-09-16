from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Cluster, Reservation, UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
				
class ClusterForm(ModelForm):
	class Meta:
		model = Cluster
		fields = ('tag_system', 'title', 'Beschreibung', 'availability')

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

#help ReservationForm so that User can only interact with date (no change to given cluster or user)
# class DateInput(forms.ModelForm):
# 	class Meta:
# 		model = Reservation
# 		fields = ['date']

# class ReservationForm(ModelForm):
# 	class Meta:
# 		model = Reservation
# 		fields = ['cluster', 'date', 'user']
# 	date = forms.DateField(
#         widget=forms.DateInput(format='%m/%d/%Y'),
#         input_formats=('%m/%d/%Y', )
#         )

class DateInput(forms.DateInput):
    input_type = 'date'

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['date']
        widgets = {
            'cluster_title': forms.TextInput(attrs= {'class': 'form-control'}),
			'date': DateInput(),
            
		}
	
class ProfileForm(forms.Form):

    email = forms.CharField(label='Email', max_length=50, required=False)
    matrikelnummer = forms.IntegerField(label='Student-ID', required=False)



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'matrikelnummer']