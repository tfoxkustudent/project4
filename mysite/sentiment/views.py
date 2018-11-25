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
        "one_item" : "document.getElementById('frame').src = '/one_item'",
        "two_item" : "document.getElementById('frame').src = '/two_item'",
        "three_item" : "document.getElementById('frame').src = '/three_item'",
        "four_item" : "document.getElementById('frame').src = '/four_item'"
    }
    return render(request, "index.html", context=context)

"""
References the about webpage for the about link in html
"""

def AboutPageView(request):
    return render(request, "about.html")

def OneItemFrame(request):
    return render(request, "one_item.html")

def TwoItemFrame(request):
    return render(request, "two_item.html")

def ThreeItemFrame(request):
    return render(request, "three_item.html")

def FourItemFrame(request):
    return render(request, "four_item.html")

"""
beta to try and figure out how to pass values through
"""
def Results(request):

    numberOfItems = request.POST["value"]

    context = {}
    positive_percentages = []
    for i in range(int(numberOfItems)):
        context = dict(context, **search(request.POST["item" + str(i + 1)], str(i + 1)))
        positive_percentages.append(float(context["positive_percentage_" + str(i + 1)]))

    context["best_item"] = context["item_" + str(positive_percentages.index(max(positive_percentages)) + 1)]

    page = { "1" : "one", "2" : "two", "3" : "three", "4" : "four" }

    return render(request, page[numberOfItems] + "_item_results.html", context=context)

def search(term, count):

    twitter_data = TwitterHandle()

    tweets = twitter_data.sort_tweets(query=term, count=200)

    positive_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "positive"]
    negative_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "negative"]
    neutral_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "neither"]

    http = urllib3.PoolManager()
    positive_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in positive_tweets]
    negative_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in negative_tweets]

    context = {
        "item_" + count : term,
        "positive_count_" + count : len(positive_tweets),
        "negative_count_" + count : len(negative_tweets),
        "neutral_count_" + count : len(neutral_tweets),
        "total_count_" + count : len(tweets),
        "positive_percentage_" + count : "{0:.2f}".format(100*len(positive_tweets)/len(tweets)),
        "negative_percentage_" + count : "{0:.2f}".format(100*len(negative_tweets)/len(tweets)),
        "neutral_percentage_" + count : "{0:.2f}".format(100*len(neutral_tweets)/len(tweets)),
        "searches_remaining_" + count : twitter_data.api_call_check(),
        "positive_html_" + count : positive_html[0:3],
        "negative_html_" + count : negative_html[0:3]
    }

    return context
