from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from sentiment.oauth import TwitterHandle
import urllib3
import json

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

    context1 = search(request.POST["name1"], 1)
    context2 = search(request.POST["name2"], 2)

    return render(request, "basic.html", context=dict(context1, **context2))

def search(term, count):

    twitter_data = TwitterHandle()

    tweets = twitter_data.sort_tweets(query=term, count=200)

    positive_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "positive"]
    negative_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "negative"]
    dont_care_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "neither"]

    http = urllib3.PoolManager()
    positive_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in positive_tweets]
    negative_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in negative_tweets]

    context = {
        "positive_count_" + str(count) : len(positive_tweets),
        "negative_count_" + str(count) : len(negative_tweets),
        "dont_care_count_" + str(count) : len(dont_care_tweets),
        "total_count_" + str(count) : len(tweets),
        "positive_percentage_" + str(count) : 100*len(positive_tweets)/len(tweets),
        "negative_percentage_" + str(count) : 100*len(negative_tweets)/len(tweets),
        "dont_care_percentage_" + str(count) : 100*len(dont_care_tweets)/len(tweets),
        "searches_remaining_" + str(count) : twitter_data.api_call_check(),
        "positive_html_" + str(count) : positive_html,
        "negative_html_" + str(count) : negative_html
    }

    return context
