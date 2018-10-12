import tweepy
from tweepy.auth import OAuthHandler
import textblob
import re

_consumer_key = 'AEhb60ATrwXNROE1kpVfDA3zD'
_consumer_secret = 'Opiv4zc6EUB58XuiakuNkkK0r9MqpXY5mbeT7YIM4CufwAGEpV'
_access_token = '1050093442393657344-phxu5UmRXJ5aIqPqFZ3PwkoBzi3EXS'
_access_token_secret ='NDpvknpSJuEU9gbpzpweldcXAhXxkV9Iqq0UAwQnUrono'

auth = OAuthHandler(_consumer_key, _consumer_secret)

auth.set_access_token(_access_token, _access_token_secret)

api = tweepy.API(auth)
api.update_status('tweepy+oauth!')
fetch_tweet = api.search(q = 'Donald Trump', count = 10)
for tweet in fetch_tweet:
    print(tweet.text)

print("this works")
