from bs4 import BeautifulSoup
import page
import requests
import unicodedata
import sys

class Categories(object):
	def __init__(self,link,depth=1,max_depth=float('inf')):
		self.base = 'https://en.wikipedia.org'
		self.link =  self.base + link
		self.subCategories = []
		self.subPages = []
		self.depth = depth
		self.max_depth = max_depth
		try:
			r = requests.get(self.link)
			self.doc = BeautifulSoup(r.content)
		except:
			print "Unexpected error:", sys.exc_info()[0]

	def getSubCategories(self):
		try:
			eachCategory = self.doc.find_all('div',class_='CategoryTreeItem')
			for sub in eachCategory:
				link = sub.a.get('href').encode('ascii','ignore')
				if isCategory(link):
					self.subCategories.append(Categories(link,self.depth + 1,self.max_depth))
		except:
			print "Unexpected error:", sys.exc_info()[0]

	def getClosestPages(self):
		try:
			pagesBlock = self.doc.find_all('div',id='mw-pages')

			if len(pagesBlock) != 1:
				raise Exception("No Page Section")

			pageDoc = pagesBlock[0]
			pageCategory = pageDoc.find_all('a')

			# print 'about to get the pages from page list of length ',len(pageCategory)
			for pageTag in pageCategory:
				pageLink = pageTag.get('href')
				strPage = pageLink.encode('ascii','ignore')
				# check to make sure the page I'm adding to the subpages list is a valid wikipedia article
				if page.isPage(strPage):
					newPage = page.Page(strPage,self.depth)
					self.subPages.append(newPage)

		except:
			print "Unexpected error:", sys.exc_info()[0]

	def collectLeafPages(self):
		self.getSubCategories()
		self.getClosestPages()
		for category in self.subCategories:
			if category.depth > self.max_depth:
				break
			childPages = category.collectLeafPages()
			self.subPages += childPages
		return self.subPages

# checks whether the type of the link is actually a category type to avoiding adding strange links
def isCategory(link):
	return link.startswith("/wiki/Category:")

