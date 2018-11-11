import unittest
from oauth import TwitterHandle

class baseTestCase(unittest.TestCase):
	def setUp(self):
		self.th = TwitterHandle()

class ParseTestCase(baseTestCase):
	# def setUp(self):
	#  	# test parser on constant tweets

	# def tearDown(self):

	def testSpaces(self):
		text = "a b c"
		check = self.th.tweet_parse(text)
		# print(check)
		assert (check == "abc")




if __name__ == "__main__":
	unittest.main()