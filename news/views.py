from django.shortcuts import render, redirect
from django.http import HttpResponse #This 'HttpResponse' will be responsible for returning a response to a user.
from django.http import Http404
import datetime as dt
from .models import Article
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
#Create your views here.

#Function that gets the weekday number for the date.
# def convert_dates(dates):
#     day_number = dt.date.weekday(dates)

#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     #Returning the actual day of the week.
#     day = days[day_number]
    
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()

    # Since the form will be submitting sensitive data to the database we are going to use a POST request.
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            print('valid')
    else:
        form = NewsLetterForm()
    
    return render(request, 'all-news/today-news.html', {"date": date,"news":news, "letterForm":form})


# View Function to present news from past days
def past_days_news(request, past_date):
    try:
        #Converts data from the string URL
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()

    except ValueError:
        #Raise 404 error when ValueError is thrown
        raise Http404()
        assert False
    
    if date == dt.date.today():
        #return redirect(news_of_day)
        return redirect(news_today)

    news = Article.days_news(date)
    #return render(request, 'all-news/past-news.html', {"date": date})
    return render(request, 'all-news/past-news.html',{"date": date,"news":news})


# View function that will handle the logic for displaying the search results
def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})


# View function for displaying a single article
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})
