import unittest
from oauth import TwitterHandle

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

if __name__ == "__main__":
	unittest.main()