from django import forms
from .models import Comment

class UnAuthCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'content')

class AuthCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)