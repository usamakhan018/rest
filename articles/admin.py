from django.contrib import admin
from .models import Article, Comment, Subscribe



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'author', 'title', 'content', 'publish', 'updated', 'tags')
	prepopulated_fields = {'slug': ('title',)}
	uneditable_fields = ('views', 'likes')

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'is_active')

@admin.register(Comment)
class ArticlAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'email', 'article', 'content', 'updated')