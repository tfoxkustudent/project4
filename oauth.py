'''
Oauth process of connecting to twitter api
'''

import tweepy
from tweepy.auth import OAuthHandler
from textblob import TextBlob as tb
import re

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
        return first.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


    def tweet_scoring_sentiment(self, tweet):

        sentiment_score = tb(self.tweet_parse(tweet))

        if sentiment_score.sentiment.polarity > 0:
            return 'positive'
        elif sentiment_score.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neither'


    def sort_tweets(self, query, count = 10):
        '''
        Grab the tweets and parse
        '''

        tweets = []
        try:
            grab_tweets = self.api.search(q = query, count = count)

            for tweet in grab_tweets:

                ready_tweets = {}

                ready_tweets['text']= tweet.text
                ready_tweets['sentiment']= self.tweet_scoring_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if ready_tweets not in tweets:
                        tweets.append(ready_tweets)

            return tweets

        except tweepy.TweepError as e:

            print("Error : " + str(e))

def main():

    con = TwitterHandle()

    tweets = con.sort_tweets(query = 'Kansas Basketball', count = 200)


    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

    print("Positive tweets percentage: {} %".format(100*len(positive_tweets)/len(tweets)))

    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Negative tweets percentage: {} %".format(100*len(negative_tweets)/len(tweets)))

    dont_care_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neither']
    print("Percentage who Dont care: {} %".format(100*len(dont_care_tweets)/len(tweets)))


    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])


    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":

    main()
