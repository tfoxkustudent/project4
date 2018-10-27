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
        return first.join(re.findall("[a-zA-Z]+", tweet))


    def tweet_scoring_sentiment(self, tweet):

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
            grab_tweets = self.api.search(q = query, count = count)

            for tweet in grab_tweets:
                if not tweet.retweeted:

                    scoring_tweets = {}

                    scoring_tweets['tweet']= tweet.text
                    scoring_tweets['score']= self.tweet_scoring_sentiment(tweet.text)

                    if tweet.retweet_count == 0:
                        if scoring_tweets not in tweets:
                            tweets.append(scoring_tweets)

            return tweets

        except tweepy.TweepError as e:

            print("Error : " + str(e))

def main():

    con = TwitterHandle()

    tweets = con.sort_tweets(query = 'Elon Musk', count = 200)

    positive_tweets = [tweet for tweet in tweets if tweet['score'] == 'positive']
    negative_tweets = [tweet for tweet in tweets if tweet['score'] == 'negative']
    dont_care_tweets = [tweet for tweet in tweets if tweet['score'] == 'neither']

    print("\nnumber of positive tweets {}".format(len(positive_tweets)))
    print("\nnumber of negative tweets {}".format(len(negative_tweets)))
    print("\nnumber of don't care tweets {}".format(len(dont_care_tweets)))
    print("\nnumber of total tweets {}".format(len(tweets)))

    print("\nPercentage of positive tweets: {} %".format(100*len(positive_tweets)/len(tweets)))
    print("\nPercentage of negative tweets: {} %".format(100*len(negative_tweets)/len(tweets)))
    print("\nPercentage who Dont care: {} %".format(100*len(dont_care_tweets)/len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['tweet'])

    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:10]:
        print(tweet['tweet'])

if __name__ == "__main__":

    main()
