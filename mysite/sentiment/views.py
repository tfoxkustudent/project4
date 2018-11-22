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
        "resize_frame" : "this.style.height = this.contentWindow.document.body.scrollHeight + 'px'"
    }
    return render(request, "index.html", context=context)

"""
References the about webpage for the about link in html
"""

def AboutPageView(request):
    return render(request, "about.html")

def TwoItemFrame(request):
    return render(request, "two_item.html")

def OneItemFrame(request):
    return render(request, "one_item.html")

"""
beta to try and figure out how to pass values through
"""

def TwoItemResults(request):

    context1 = search(request.POST["item1"], 1)
    context2 = search(request.POST["item2"], 2)

    context = dict(context1, **context2)

    if float(context["positive_percentage_1"]) > float(context["positive_percentage_2"]):
        context["best_item"] = context["item_1"]
    else:
        context["best_item"] = context["item_2"]

    return render(request, "two_item_results.html", context=context)

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
        "item_" + str(count) : term,
        "positive_count_" + str(count) : len(positive_tweets),
        "negative_count_" + str(count) : len(negative_tweets),
        "neutral_count_" + str(count) : len(neutral_tweets),
        "total_count_" + str(count) : len(tweets),
        "positive_percentage_" + str(count) : "{0:.2f}".format(100*len(positive_tweets)/len(tweets)),
        "negative_percentage_" + str(count) : "{0:.2f}".format(100*len(negative_tweets)/len(tweets)),
        "neutral_percentage_" + str(count) : "{0:.2f}".format(100*len(neutral_tweets)/len(tweets)),
        "searches_remaining_" + str(count) : twitter_data.api_call_check(),
        "positive_html_" + str(count) : positive_html[0:3],
        "negative_html_" + str(count) : negative_html[0:3]
    }

    return context
