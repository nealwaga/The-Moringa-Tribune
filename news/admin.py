from django.contrib import admin
# from .models import Editor,Article,tags
from .models import *

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal =('tags',)

# admin.site.register(Editor)
admin.site.register(Article, ArticleAdmin)
admin.site.register(tags)
