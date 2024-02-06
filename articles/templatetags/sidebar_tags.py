from django import template
from ..models import Article

register = template.Library()

@register.simple_tag
def total_posts():
	return Article.objects.count()

@register.inclusion_tag('articles/tags/recent_articles.html')
def latest_articles(count=3):
	latest_articles = Article.objects.order_by('-updated')[:count]
	return {'latest_articles': latest_articles}

@register.filter
def add_class(field, class_name):
	return field.as_widget(attrs={"class": " ".join((field.css_classes(), class_name))})
