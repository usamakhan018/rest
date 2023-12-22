from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Account
from .forms import LoginForm, RegisterForm, UpdateForm
from django.contrib.auth.decorators import login_required

@login_required
def account_view(request, user_id):
	context = {}
	user = request.user
	try:
		account = Account.objects.get(id=user_id)
	except Account.DoesNotExist:
		return HttpResponse("Account with this id is not found.")

	context['account'] = account
	return render(request, 'account/account.html', context)

def login_view(request):
	context = {}
	if request.user.is_authenticated:
		return redirect('articles:home')
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect('articles:home')
	else:
		form = LoginForm()
		context['form'] =form
	return render(request, 'account/login.html', context)

@login_required
def logout_view(request):
	logout(request)
	return redirect('articles:home')

def register_view(request):
	context = {}
	if request.user.is_authenticated:
		return redirect('articles:home')
	if request.method == 'POST':
		form = RegisterForm(data=request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			return redirect('articles:home')
	else:
		form = RegisterForm()
		context['form'] = form
	return render(request, 'account/register.html', context)

@login_required
def update_view(request):
	context = {}
	if request.method == 'POST':
		form = UpdateForm(data=request.POST, instance=request.user, files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect('articles:home')
	else:
		form = UpdateForm(instance=request.user)
		context['form'] = form
	return render(request, 'account/update.html', context)