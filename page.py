from bs4 import BeautifulSoup
import requests
import unicodedata
import sys
import re
from nltk.corpus import stopwords


"""
A Page object will represent a normal wikipedia entry

Link: string in the form "/wiki/example_page"
depth: integer used by categories to keep track of how deep the page is
		and also can be used later in classification if we want to weigh
		pages on how far they are away from the root Category

"""
class Page(object):
	def __init__(self,link,depth=1):
		self.depth = depth
		self.base = 'https://en.wikipedia.org'
		self.link = self.base + link
		self.words = {}
		self.links = []
		self.depth = depth
		try:
			r = requests.get(self.link)
			self.doc = BeautifulSoup(r.content)
			self.getLinks()
			self.getWords()
		except:
			print "Unexpected error:", sys.exc_info()[0]

	"""
	This method collects all words in a documents and stores them in a dictionary
	where the key is the lowercase version of the word stripped of all non alphabet characters
	and the value is the number of occurences
	"""
	def getWords(self):
		stops = set(set(stopwords.words('english')))
		bodyContent = self.doc.find_all('div',id='bodyContent')
		if len(bodyContent) != 1:
			raise Exception("no body content")

		contentString = bodyContent[0].get_text().encode('ascii','ignore')
		contentList = contentString.split()
		for item in contentList:
			item = re.sub('[^a-zA-Z]+', '', item)
			lowerItem = item.lower()
			if (lowerItem not in stops) and (lowerItem in self.words):
				self.words[lowerItem] += 1
			elif lowerItem not in stops:
				self.words[lowerItem] = 1
		if "" in self.words:
			self.words.pop("")

		return self.words

	"""
	This method retreives all of wikipedia page links on a page and stores them as strings
	since we won't be recursing on them later. I could potentially have them stored as pages themselves,
	but I felt this to be unnecessary for my current use. 
	"""
	def getLinks(self):
		bodyContentList = self.doc.find_all('div',id='bodyContent')
		if len(bodyContentList) != 1:
			raise Exception("no body content")

		bodyContent = bodyContentList[0]
		linksTagged = bodyContent.find_all('a')
		for tag in linksTagged:
			linkAscii = tag.get('href')
			link = linkAscii.encode('ascii','ignore')
			if isPage(link):
				self.links.append(link)
		return self.links


"""
the same as the isCateory function, this is a simple check on the string format of the 
given page to make sure it is relvant to wikipedia. There exists more sophisticated checks, but
I feel this is the most time effecient
"""
def isPage(link):
	return (not link.startswith("/wiki/Category:")) and (link.startswith("/wiki/"))