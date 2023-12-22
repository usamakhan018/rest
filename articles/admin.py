from django.contrib import admin
from .models import Article, Comment

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'title', 'content', 'publish', 'updated', 'tags')
	prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class ArticlAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'article', 'subject', 'content', 'updated')
