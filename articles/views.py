from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import AuthCommentForm,UnAuthCommentForm
from .models import Article, Comment, Subscribe
from account.models import Account
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from articles.decorators import ajax_required
from django.http import JsonResponse, HttpResponse

def account_view(request, user_id):
	context = {}
	account = Account.objects.get(pk=user_id)
	context['account'] = account
	return render(request, 'account/account.html', account)



def home_view(request, tag=None, author=None):
	context = {}
	if tag:
		articles = Article.published.filter(tags__slug=tag)
	else:
		articles = Article.published.all()
	
	paginator = Paginator(articles, 4)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except EmptyPage:
		articles = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		articles = paginator.page(1)

	context['articles'] = articles
	return render(request, 'articles/home.html', context)


def detail_view(request, year, month, day, slug):
	context = {}
	article = Article.published.get(publish__year=year, publish__month=month, publish__day=day, slug=slug)
	comments = Comment.objects.filter(article=article, is_active=True)
	if request.method == 'POST':
		if request.user.is_authenticated:
			form = AuthCommentForm(data=request.POST)
		else:
			form = UnAuthCommentForm(data=request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.article = article
			if not new_comment.email:
				new_comment.name = request.user.username
				new_comment.email = request.user.email

			new_comment.save()
			messages.success(request, 'comment submitted succesfully')
			return redirect(article.get_absolute_url())
	else:
		if request.user.is_authenticated:
			form = AuthCommentForm(instance=request.user)
		else:
			form = UnAuthCommentForm()
	post_tags_ids = article.tags.values_list('id', flat=True)
	related_articles = Article.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
	related_articles = related_articles.annotate(similar_articles=Count('tags')).order_by('similar_articles', '-publish')[:3]
	if not related_articles:
		related_articles = Article.published.all()[:3]
	context['article'] = article
	context['comment_form'] = form
	context['comments'] = comments
	context['related_articles'] = related_articles
	article.views = article.views + 1
	article.save()
	return render(request, 'articles/detail.html', context)

def search_view(request):
	context = {}
	query = request.GET.get('q')
	if query:
		articles = Article.objects.annotate(search=SearchVector('title', 'author__username')).filter(search=query)
		context['articles'] = articles
	return render(request, 'articles/search.html', context)


def subscription_view(request):
	print("in view")
	if request.method == 'POST':
		form = SubscriptionForm(data=request.POST)
		print("form get")
		if form.is_valid():
			form.save()
			print("formsaved")
			messages.success(request, "subscription successfull you will receive an email at every update")
			return redirect('/')


@ajax_required
def like_view(request):
	if not request.user.is_authenticated:
		return JsonResponse({"status": "error", "header": "autu error" ,"data": "please login to like article"})
	if not request.user.is_active:
		return JsonResponse({"status": "error", "header": "Activation", "data": "please activate your account"})
	article_id = request.POST.get('article_id')
	action = request.POST.get('action')
	try:
		article = Article.objects.get(pk=article_id)
	except Article.DoesNotExist:
		return JsonResponse({'status': 'error', 'action': action})

	if action == 'like':
		article.likes.add(request.user)
	elif action == 'unlike':
		article.likes.remove(request.user)
	return JsonResponse({'status': 'ok', 'action': action})

@ajax_required
def subscribe_view(request):
	if not request.user.is_authenticated:
		return JsonResponse({"status": "error", "header": "autu error" ,"data": "please login to like article"})
	if not request.user.is_active:
		return JsonResponse({"status": "error", "header": "Activation", "data": "please activate your account"})

	email = request.POST.get('email')
	if email:

		try:
			email = Subscribe.objects.get(email=email)

		except Subscribe.DoesNotExist:
			Subscribe.objects.create(email=email)
			return JsonResponse({"status": "ok", "header": "Success", "data": "you have successfully subscribed to our email list"})
		if email.is_active:
			return JsonResponse({"status": "ok", "header": "Success", "data": "you've already subscribed."})
		email.is_active = True
		email.save()
	else:
		return JsonResponse({"status": "ok", "header": "Email", "data": "Problem with email"})	
	return JsonResponse({"status": "ok", "header": "Success", "data": "your subscription has been activated"})
	