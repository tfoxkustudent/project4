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
		'''
		checks if parsing maintains internal spaces
		'''
		text = "a b c"
		check = self.th.tweet_parse(text)
		assert (check == "a b c")
	

	def testPositive(self):
		'''
		tests known positive string
		'''
		text = "good"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'positive')

	def testNegative(self):
		'''
		tests known negative string
		'''
		text = "bad"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'negative')
	
	def testEmpty(self):
		'''
		tests empty string
		'''
		text = ""
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'neither')

	def testNeither(self):
		'''
		test several neutral words
		'''
		text = "the person and or"
		check = self.th.tweet_scoring_sentiment(text)
		assert(check == 'neither')

class TweepyTestCase(baseTestCase):
	def testCallCheck(self):
		'''
		tests that checking number of search calls doesn't change it
		'''
		a = self.th.api_call_check()
		b = self.th.api_call_check()
		assert((a-b) == 0)
	def testSearchCheck(self):
		'''
		tests that call_check updates after calls
		'''
		a = self.th.api_call_check()
		tweets = self.th.sort_tweets(query = 'Elon Musk', count = 50)
		b = self.th.api_call_check()
		assert((a-b) > 0)

if __name__ == "__main__":
	unittest.main()