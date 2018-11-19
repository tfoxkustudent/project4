import unittest
from oauth import TwitterHandle
import tweepy

class baseTestCase(unittest.TestCase):
	def setUp(self):
		self.th = TwitterHandle()

class ParseTestCase(baseTestCase):
	# def setUp(self):
	#  	# test parser on constant tweets

	# def tearDown(self):

	def testSpaces(self): #Test - not remioving interior spaces TODO confirm how textblob works
		text = "a b c"
		check = self.th.tweet_parse(text)
		# print(check)
		assert (check == "a b c")
		
	# def testRetweets(self):

	def testPositive(self):
		text = "good"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'positive')

	def testNegative(self):
		text = "bad"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'negative')
	
	def testEmpty(self):
		text = ""
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'neither')

	def testNeither(self):
		text = "the person and or"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'neither')

class TweepyTestCase(baseTestCase):
	def testCallCheck(self):
		a = self.th.api_call_check()
		b = self.th.api_call_check()
		assert((a-b) == 0)
	def testSearchCheck(self):
		a = self.th.api_call_check()
		tweets = self.th.sort_tweets(query = 'Elon Musk', count = 50)
		b = self.th.api_call_check()
		assert((a-b) > 0)
	def testRetweet(self):
		grab_tweets = tweepy.Cursor(self.th.api.search,q = 'Elon Musk', count = 50).items(50)
		for tweet in grab_tweets:
			if not tweet.retweeted:
				assert(tweet.retweet_count == 0)

if __name__ == "__main__":
	unittest.main()