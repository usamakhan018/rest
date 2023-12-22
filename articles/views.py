from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .forms import CommentForm
from .models import Article, Comment
from django.contrib.postgres.search import SearchVector
from django.db.models import Count

def home_view(request, tag=None):
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
		form = CommentForm(data=request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.article = article
			new_comment.save()
			messages.success(request, 'comment submitted succesfully')
			return redirect(article.get_absolute_url())
	else:
		if request.user.is_authenticated:
			form = CommentForm(instance=request.user)
		form = CommentForm()
	post_tags_ids = article.tags.values_list('id', flat=True)
	related_articles = Article.published.filter(tags__in=post_tags_ids).exclude(id=article.id)
	related_articles = related_articles.annotate(similar_articles=Count('tags')).order_by('similar_articles', '-publish')[:3]
	if not related_articles:
		related_articles = Article.published.all()[:3]
	context['article'] = article
	context['comment_form'] = form
	context['comments'] = comments
	context['related_articles'] = related_articles
	return render(request, 'articles/detail.html', context)

def search_view(request):
	context = {}
	query = request.GET.get('q')
	if query:
		articles = Article.objects.annotate(search=SearchVector('author','title')).filter(search=query)
		context['articles'] = articles
	return render(request, 'articles/search.html', context)