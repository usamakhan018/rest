from django import forms
from account.models import Account
from django.contrib.auth import authenticate


class LoginForm(forms.ModelForm):
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	class Meta:
		model = Account
		fields = ('username', 'password')

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if not authenticate(username=username, password=password):
			raise forms.ValidationError('invalid login credentials')

class RegisterForm(forms.ModelForm):
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	password2 = forms.CharField(label="repeat password", max_length=255, widget=forms.PasswordInput)
	class Meta:
		model = Account
		fields = ('username', 'email', 'password', 'password2')	

	def clean_password2(self):
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if not password == password2:
			raise forms.ValidationError('Passwords are not same.')
		return password2


class UpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('username', 'email', 'first_name', 'last_name', 'hide_email', 'profile_image')