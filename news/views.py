from django.shortcuts import render
from django.http import HttpResponse #This 'HttpResponse' will be responsible for returning a response to a user.
from django.http import Http404
import datetime as dt
from django.shortcuts import render

#Create your views here.
def welcome(request):
    #return HttpResponse('Welcome to the Moringa Tribune!')
    return render (request, 'welcome.html')


def news_of_day(request):
    date = dt.date.today()

    #Function to convert date object to find the exact day.
    day = convert_dates(date)
    html = f'''
        <html>
            <body>
                <h1> News for {day} {date.day}-{date.month}-{date.year} </h1>
            <body>
        <html>
            '''
    return HttpResponse(html)


def convert_dates(dates):
    #Function that gets the weekday number for the date.
    day_number = dt.date.weekday(dates)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    #Returning the actual day of the week.
    day = days[day_number]
    

def past_days_news(request, past_date):
    try:
        #Converts data from the string URL
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()

    except ValueError:
        #Raise 404 error when ValueError is thrown
        raise Http404()

    day = convert_dates(date)
    html = f'''
        <html>
            <body>
                <h1> News for {day} {date.day}-{date.month}-{date.year} <h1>
            <body>
        <html>
            '''
    return HttpResponse(html)