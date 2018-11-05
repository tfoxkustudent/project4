from django.shortcuts import render, redirect
from django.views.generic import TemplateView
#from sentiment.forms import HomeForm
from sentiment.oauth import TwitterHandle
# Create your views here.

"""
References the index.html when website starts up
"""

def HomePageView(request):
    return render(request, "index.html")

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
        "search_results" :
            "number of positive tweets {}".format(len(positive_tweets)) +
            "\nnumber of negative tweets {}".format(len(negative_tweets)) +
            "\nnumber of don't care tweets {}".format(len(dont_care_tweets)) +
            "\nnumber of total tweets {}".format(len(tweets)) +
            "\nPercentage of positive tweets: {} %".format(100*len(positive_tweets)/len(tweets)) +
            "\nPercentage of negative tweets: {} %".format(100*len(negative_tweets)/len(tweets)) +
            "\nPercentage who Dont care: {} %".format(100*len(dont_care_tweets)/len(tweets)) +
            "\n\n REMAINING SEARCHES FOR NEXT 15 MINUTES: {}".format(twitter_data.api_call_check())
    }

    # print("\n\nPositive tweets:")
    # for tweet in positive_tweets[:10]:
    #     print(tweet['tweet'])
    #
    # print("\n\nNegative tweets:")
    # for tweet in negative_tweets[:10]:
    #     print(tweet['tweet'])

    return render(request, "basic.html", context=context)
