# from django.conf.urls import url 
from django.urls import re_path, include
#from .views import *
from . import views 
from django.conf import settings
from django.conf.urls.static import static

#We surround the date regex pattern with brackets so that we can capture it and send it to our view function.
urlpatterns=[
    #url('^$',views.welcome,name = 'welcome'),
    #url('^today/$', views.news_of_day, name = 'newsToday'),
    re_path(r'^$', views.news_today, name = 'newsToday'),
    re_path(r'^archives/(\d{4}-\d{2}-\d{2})/$', views.past_days_news, name = 'pastNews'), 
    re_path(r'^search/', views.search_results, name='search_results'), #a URLpattern that references the search_results
    re_path(r'^article/(\d+)',views.article,name ='article'), #route to display a single article
    re_path(r'^new/article$', views.new_article, name='new-article'),
    ]

if settings.DEBUG:
    urlpatterns+= static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)