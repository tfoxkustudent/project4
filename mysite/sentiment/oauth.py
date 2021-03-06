'''
These are our backend functions.  It begins with connecting to twitter API, grabbing tweets, and performing sentimental analysis.
'''
import json
import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob as tb
import re
##from django import HttpRequest

class TwitterHandle(object):

    def __init__(self):
        '''
        initialization/ connect with twitter api
        '''
        _consumer_key = 'AEhb60ATrwXNROE1kpVfDA3zD'
        _consumer_secret = 'Opiv4zc6EUB58XuiakuNkkK0r9MqpXY5mbeT7YIM4CufwAGEpV'
        _access_token = '1050093442393657344-phxu5UmRXJ5aIqPqFZ3PwkoBzi3EXS'
        _access_token_secret ='NDpvknpSJuEU9gbpzpweldcXAhXxkV9Iqq0UAwQnUrono'
        try:
            self.auth = OAuthHandler(_consumer_key, _consumer_secret)

            self.auth.set_access_token(_access_token, _access_token_secret)

            self.api = tweepy.API(self.auth)
        except:
            print("Could not connect with twitter API")

    def tweet_parse(self, tweet):
        '''
        Parse tweets so we can send through natural language library
        '''
        first = ' '
        parser = first.join(re.findall("[a-zA-Z]+", tweet)) #XXX why don't we use strip() before return?
        return parser


    def tweet_scoring_sentiment(self, tweet):
        '''
        Scoring tweets and storing them depending on their sentiment
        '''
        sentiment_score = tb(self.tweet_parse(tweet).strip())

        if sentiment_score.sentiment.polarity > 0:
            return 'positive'
        elif sentiment_score.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neither'


    def sort_tweets(self, query, count):
        '''
        Grab the tweets and parse
        '''

        tweets = []
        try:
            grab_tweets = tweepy.Cursor(self.api.search,q = query, count = count).items(300)

            for tweet in grab_tweets:
                if not tweet.retweeted:

                    scoring_tweets = {}

                    scoring_tweets['tweet'] = tweet.text
                    scoring_tweets['score'] = self.tweet_scoring_sentiment(tweet.text)
                    scoring_tweets['id'] = tweet.id

                    if tweet.retweet_count == 0:
                        if scoring_tweets not in tweets:
                            tweets.append(scoring_tweets)

            return tweets

        except tweepy.TweepError as e:

            print("Error : " + str(e))

    def api_call_check(self):
        '''
        returns our searches remaining per 15 minutes
        '''
        rate_limit = self.api.rate_limit_status()

        return rate_limit["resources"]["search"]["/search/tweets"]["remaining"]

