from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Account, Contact
from articles.models import Article
from .forms import LoginForm, RegisterForm, UpdateForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from articles.decorators import ajax_required

def account_view(request, user_id):
	context = {}
	user = request.user
	try:
		account = Account.objects.get(id=user_id)
		articles_liked = Article.objects.filter(likes=account)
		my_articles = Article.objects.filter(author=account)
		print(articles_liked)
	except Account.DoesNotExist:
		return HttpResponse("Account with this id is not found.")

	is_self = None

	if user == account:
		is_self = True


	context['account'] = account
	context['is_self'] = is_self
	context['articles_liked'] = articles_liked
	context['my_articles'] = my_articles
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
			new_user.is_active = False
			new_user.save()

			subject = "we've sent you an email containing the activation link please follow the instructions to activate your account"
			message = render_to_string('account/activation_email.html', {
					'user': new_user,
					'token': activation_token.make_token(new_user),
					'uid': urlsafe_base64_encode(force_bytes(new_user.id)),
				})

			email = EmailMessage(subject, message, to=[form.cleaned_data['email']])
			email.send()
			return redirect('articles:home')
	else:
		form = RegisterForm()
	
	context['form'] = form
	return render(request, 'account/register.html', context)

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		account = Account.objects.get(id=uid)
	except Exception as e:
		raise e
	
	if activation_token.check_token(account, token):
		account.is_active = True
		account.save()
		return redirect('articles:home')
	

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

@ajax_required
def follow_view(request):
	user = request.user
	if not user.is_authenticated:
		return JsonResponse({'status': 'error', 'header': 'Auth Error', 'data': 'please login to follow'})
	if not user.is_active:
		return JsonResponse({'status': 'error', 'header': 'Activation', 'data': 'please activate your account to fully use the application'})
	if request.method == 'POST':
		action = request.POST.get('action')
		account_id = request.POST.get('account_id')
		try:
			account = Account.objects.get(pk=account_id)
		except Account.DoesNotExist:
			return JsonResponse({'status': 'error', 'header': 'Not Found', 'data': 'account for id does not exist'})

		if action == 'follow':
			Contact.objects.get_or_create(user_from=user, user_to=account)
			return JsonResponse({'status': 'ok', 'header': 'success', 'data': 'follow'})			
		elif action == 'unfollow':
			Contact.objects.filter(user_from=user, user_to=account).delete()
			return JsonResponse({'status': 'ok', 'header': 'success', 'data': 'unfollow'})

	return JsonResponse({'status': 'error', 'header': 'Error', 'data': 'something really bad happened'})			
