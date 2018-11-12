from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from sentiment.forms import HomeForm
from sentiment.oauth import TwitterHandle
# Create your views here.

"""
References the index.html when website starts up
"""

def HomePageView(request):
    context = {
        "election" : "document.getElementById('frame').src = '/election'",
        "stocks" : "document.getElementById('frame').src = '/stocks'",
        "resize_frame" : "this.style.height = this.contentWindow.document.body.scrollHeight + 'px'"
    }
    return render(request, "index.html", context=context)

"""
References the about webpage for the about link in html
"""

def AboutPageView(request):
    return render(request, "about.html")

def ElectionFrame(request):
    return render(request, "election.html")

def StocksFrame(request):
    return render(request, "stocks.html")

"""
beta to try and figure out how to pass values through
"""

def BasicPageView(request):
    twitter_data = TwitterHandle()

    tweets = twitter_data.sort_tweets(query = request.POST["name1"], count = 200)

    positive_tweets = [tweet for tweet in tweets if tweet['score'] == 'positive']
    negative_tweets = [tweet for tweet in tweets if tweet['score'] == 'negative']
    dont_care_tweets = [tweet for tweet in tweets if tweet['score'] == 'neither']

    context = {
        "positive_tweets" : len(positive_tweets),
        "negative_tweets" : len(negative_tweets),
        "dont_care_tweets" : len(dont_care_tweets),
        "total_tweets" : len(tweets),
        "positive_percentage" : 100*len(positive_tweets)/len(tweets),
        "negative_percentage" : 100*len(negative_tweets)/len(tweets),
        "dont_care_percentage" : 100*len(dont_care_tweets)/len(tweets),
        "searches_remaining" : twitter_data.api_call_check()
    }

    # print("\n\nPositive tweets:")
    # for tweet in positive_tweets[:10]:
    #     print(tweet['tweet'])
    #
    # print("\n\nNegative tweets:")
    # for tweet in negative_tweets[:10]:
    #     print(tweet['tweet'])

    return render(request, "basic.html", context=context)
