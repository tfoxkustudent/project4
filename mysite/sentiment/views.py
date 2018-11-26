from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from sentiment.oauth import TwitterHandle
import urllib3
import json

# Create your views here.

def HomePageView(request):
    """
    References the homepage when website starts up and controls links within the iframe
    """
    context = {
        "one_item" : "document.getElementById('frame').src = '/one_item'",
        "two_item" : "document.getElementById('frame').src = '/two_item'",
        "three_item" : "document.getElementById('frame').src = '/three_item'",
        "four_item" : "document.getElementById('frame').src = '/four_item'"
    }
    return render(request, "index.html", context=context)


def AboutPageView(request):
    """
    References the about page
    """
    return render(request, "about.html")

def OneItemFrame(request):
    """
    References the one-item search
    """
    return render(request, "one_item.html")

def TwoItemFrame(request):
    """
    References the two-item search
    """
    return render(request, "two_item.html")

def ThreeItemFrame(request):
    """
    References the three-item search
    """
    return render(request, "three_item.html")

def FourItemFrame(request):
    """
    References the four-item search
    """
    return render(request, "four_item.html")

def Results(request):
    """
    References the results page, adjusting based on the number of items
    """

    numberOfItems = int(request.POST["value"])

    try:
        context = {}
        positive_percentages = []
        for i in range(numberOfItems):
            context = dict(context, **search(request.POST["item" + str(numberOfItems - i)], numberOfItems - i))
            positive_percentages.append(float(context["positive_percentage_" + str(numberOfItems - i)]))

        context["best_item"] = context["item_" + str(positive_percentages.index(max(positive_percentages)) + 1)]

        page = { 1 : "one", 2 : "two", 2 : "three", 4 : "four" }

        return render(request, page[numberOfItems] + "_item_results.html", context=context)

    except RuntimeError:
        return render(request, "error.html")

def search(term, count):
    """
    Searches twitter for the given term and returns the results
    """

    twitter_data = TwitterHandle()

    searches_remaining = twitter_data.api_call_check()

    if searches_remaining < count:
        raise RuntimeError()

    tweets = twitter_data.sort_tweets(query=term, count=200)

    countstr = str(count)

    if len(tweets) == 0:
        return {
            "item_" + countstr : term,
            "positive_count_" + countstr : 0,
            "negative_count_" + countstr : 0,
            "neutral_count_" + countstr : 0,
            "total_count_" + countstr : 0,
            "positive_percentage_" + countstr : "0.00",
            "negative_percentage_" + countstr : "0.00",
            "neutral_percentage_" + countstr : "0.00",
            "positive_html_" + countstr : [],
            "negative_html_" + countstr : [],
            "searches_remaining_" + countstr : searches_remaining,
        }

    positive_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "positive"]
    negative_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "negative"]
    neutral_tweets = [tweet["id"] for tweet in tweets if tweet["score"] == "neither"]

    http = urllib3.PoolManager()
    positive_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in positive_tweets]
    negative_html = [json.loads(http.request("GET", "https://api.twitter.com/1.1/statuses/oembed.json?id=" + str(id)).data.decode("utf-8"))["html"] for id in negative_tweets]

    context = {
        "item_" + countstr : term,
        "positive_count_" + countstr : len(positive_tweets),
        "negative_count_" + countstr : len(negative_tweets),
        "neutral_count_" + countstr : len(neutral_tweets),
        "total_count_" + countstr : len(tweets),
        "positive_percentage_" + countstr : "{0:.2f}".format(100*len(positive_tweets)/len(tweets)),
        "negative_percentage_" + countstr : "{0:.2f}".format(100*len(negative_tweets)/len(tweets)),
        "neutral_percentage_" + countstr : "{0:.2f}".format(100*len(neutral_tweets)/len(tweets)),
        "positive_html_" + countstr : positive_html[0:3],
        "negative_html_" + countstr : negative_html[0:3],
        "searches_remaining_" + countstr : searches_remaining
    }

    return context
