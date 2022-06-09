from django.shortcuts import render, redirect
from django.http import HttpResponse #This 'HttpResponse' will be responsible for returning a response to a user.
from django.http import Http404, HttpResponseRedirect
import datetime as dt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .email import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse

from rest_framework.response import Response #'Response' to handle the response for the API requests
from rest_framework.views import APIView #'APIView' as a base class for our API view function
from .models import MoringaMerch
from .serializer import MerchSerializer

#Create your views here. 
def news_today(request):
    date = dt.date.today()
    news = Article.todays_news()
    form = NewsLetterForm() #display form

    # Since the form will be submitting sensitive data to the database we are going to use a POST request.
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('news_today')
    else:
        form = NewsLetterForm()
    
    return render(request, 'all-news/today-news.html', {"date": date, "news":news, "letterForm":form})


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
@login_required(login_url='/accounts/login/')
def article(request,article_id):
    try:
        article = Article.objects.get(id = article_id)
    except ObjectDoesNotExist:
        raise Http404()
    return render(request,"all-news/article.html", {"article":article})

def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})


#view function that will get the name and email from my AJAX request, save the user in the database and sends the welcome email
def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

#a get method where we query the database to get all the MoringaMerchobjects
class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True) #serialize the Django model objects and return the serialized data as a response
        return Response(serializers.data)