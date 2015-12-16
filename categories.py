from bs4 import BeautifulSoup
import page
import requests
import unicodedata
import sys


"""
Creating a Category type which represents the a wikipedia category.
Constructor:

link: a string of the form '/wiki/Category:Example_Category'
depth: positive integer this is used internally so that each category knows how far it is from the root category 
		because categories will be made recursively as a result of other categories methods.

max_depth: positive integer. When collecting leaf pages of a category, we may only want to traverse so far into
			these pages since each cateogry has both subpages and subCategories and each of those subCategories 
			has subpages of its own. The max_depth will cap off and not consider pages deeper than max_depth.

output: Categories type object

"""
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


	"""
	Calling this method on a valid Categories type object will then retreive and store all the 
	sub categories on that page in the self.subCategories list. Each will stored in the list as a
	Categories type itself as well.

	This method should be considered a private method since calling it multiple times will add the category
	multiple times to the list

	"""
	def getSubCategories(self):
		try:
			eachCategory = self.doc.find_all('div',class_='CategoryTreeItem')
			for sub in eachCategory:
				link = sub.a.get('href').encode('ascii','ignore')
				if isCategory(link):
					self.subCategories.append(Categories(link,self.depth + 1,self.max_depth))
		except:
			print "Unexpected error:", sys.exc_info()[0]


	"""
	self.getClosestPages() will perform the same action as getSubCategories except with the closest subPages on
	the category

	Again, this should be considered a private method and not be called multiple times to avoid adding the page
	to the list multiple times and therefore messing up the count in our later naive bayes methods
	"""
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

	"""
	This method will recursively collect all the subpages related to a given category and will only traverse as far as the
	max depth allows. 
	"""
	def collectLeafPages(self):
		self.getSubCategories()
		self.getClosestPages()
		for category in self.subCategories:
			if category.depth > self.max_depth:
				break
			childPages = category.collectLeafPages()
			self.subPages += childPages
		return self.subPages

"""
This function takes in a link suffix and returns whether it is a suffix representing a category pageCategory

**NOTE**
This method can be updated to do a more sophisticated check, but I opted to only check the string format for speed. I wanted to 
reduce the number of requests made to the URL. I can see fixing this by creating and returning and HTML document of the page if 
it is valid and False otherwise that way I wouldn't have to ping it, check, then let the method make another request.

"""
def isCategory(link):
	return link.startswith("/wiki/Category:")

