from bs4 import BeautifulSoup
import requests
import unicodedata
import sys

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
		except:
			print "Unexpected error:", sys.exc_info()[0]

	def getWords(self):
		bodyContent = self.doc.find_all('div',id='bodyContent')
		if len(bodyContent) != 1:
			raise Exception("no body content")

		contentString = bodyContent[0].get_text().encode('ascii','ignore')
		contentList = contentString.split()
		for item in contentList:
			lowerItem = item.lower()
			if lowerItem in self.words:
				self.words[lowerItem] += 1
			else:
				self.words[lowerItem] = 1

		return self.words


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


def isPage(link):
	return (not link.startswith("/wiki/Category:")) and (link.startswith("/wiki/"))