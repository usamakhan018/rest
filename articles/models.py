from django.db import models
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

class ArticleManager(models.Manager):
	def get_queryset(self):
		return super(ArticleManager, self).get_queryset().filter(status='published')


class Article(models.Model):
	STATUS_CHOICE = (
		('published', 'Published'), 
		('draft', 'Draft'), 
		)

	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)
	title = models.CharField(max_length=500)
	slug = models.SlugField(max_length=500)
	featured_image = models.ImageField(upload_to='article_images/%y/%m/%d/', null=True, blank=True)
	content = RichTextUploadingField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

	views = models.PositiveIntegerField(default=0)
	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles_liked')	

	tags = TaggableManager()
	objects = models.Manager()
	published = ArticleManager()
	def __str__(self):
		return f"{self.author} posted {self.title}"

	def get_absolute_url(self):
		return reverse('articles:detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
	article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	content = models.TextField()
	
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.name} commented on {self.article}"

class Subscribe(models.Model):
	email = models.EmailField(max_length=255)
	is_active = models.BooleanField(default=True)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.email}"