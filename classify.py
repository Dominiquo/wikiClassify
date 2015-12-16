import categories
import page
from bs4 import BeautifulSoup
import page
import requests
import sqlite3
import unicodedata
import sys

"""
Creating a classifer based on the links from the leaf pages. 

***INPUT***

categoriesLinks: List of Strings. This is a list of the links that represent the categories we want to use as 
					as our classification. Again, this is only the suffix of the full URL

useLinks: Boolean indicating whether we will be creating our probabilites on either the bag of all words on the page
			or the links that occur on the page.

max_depth: Integer. How far do we want our crawling to actually traverse from these root nodes? Specify here, but 
			be aware that the number of pages has the potential to grow exponentially with the depth.

***OUTPUT***
allCatsLinks: a list of strings that will be used as a reference to which row represents which cateogry page in the next return val

occurMatrix: a nxm matrix where there are N valid given categories (N rows) and M different links that appear in the union of all the 
			leaf pages of categories. Each i,j represents the number of occurence of a given link in that category

totals: list of integers of length M that represets the total number of occurences of a link across all of the categoreies leaf pages 

keyDict: a dictionary where the key is a string of the form "wiki/example_page" and the value is a number i 0<= i <= m i.e the value 
		is the index in the matrix and total vector that represents the number of occurences of the key (link). 
"""
def createClassifier(categoriesLinks,useLinks=True,max_depth=1):
	allCategories = [] #will be used to store the categories types of the initial links
	allCatsLinks = [] #basically a copy of the categoriesLinks, but we move over tho this list if any were invalid
	base = 'https://en.wikipedia.org'
	key = []
	keyDict = {}
	for link in categoriesLinks:
		if categories.isCategory(link):
			allCatsLinks.append(link)
			allCategories.append(categories.Categories(link,1,max_depth))

	occurMatrix = []
	totals = []
	max_cat = 0
	if useLinks:
		for cat in allCategories:
			cat.collectLeafPages()
			catOccurences = [0]*max_cat
			# print 'length of subpages is ', len(cat.subPages)
			for pg in cat.subPages:
				for link in pg.links:
					if link not in keyDict:
						keyDict[link] = max_cat
						catOccurences.append(1)
						totals.append(1)
						max_cat += 1
					else:
						index = keyDict[link]
						catOccurences[index] += 1
						totals[index] += 1
			occurMatrix.append(catOccurences)
			# print 'the current maximum number of categories is',max_cat,'for category',cat.link

		for row in occurMatrix:
			row += [0]*(max_cat - len(row))
	else:
		for cat in allCategories:
				cat.collectLeafPages()
				catOccurences = [0]*max_cat
				for pg in cat.subPages:
					for word,n in pg.words.iteritems():
						if word not in keyDict:
							keyDict[word] = max_cat
							catOccurences.append(n)
							totals.append(n)
							max_cat += 1
						else:
							index = keyDict[word]
							catOccurences[index] += n
							totals[index] += n
				occurMatrix.append(catOccurences)

			for row in occurMatrix:
				row += [0]*(max_cat - len(row))

	return allCatsLinks,occurMatrix,totals,keyDict

"""
This classifier takes as input, the output of the prior probabilites generated in the createClassifier function therefore making it 
easier to classify a page if the prior probabilites have already been serialized.

***INPUT***
classPage: Page type representing a wikipedia page that we want to classify

allCatsLinks: a list of strings that will be used as a reference to which row represents which cateogry page in the next return val

occurMatrix: a nxm matrix where there are N valid given categories (N rows) and M different links that appear in the union of all the 
			leaf pages of categories. Each i,j represents the number of occurence of a given link in that category

totals: list of integers of length M that represets the total number of occurences of a link across all of the categoreies leaf pages 

keyDict: a dictionary where the key is a string of the form "wiki/example_page" and the value is a number i 0<= i <= m i.e the value 
		is the index in the matrix and total vector that represents the number of occurences of the key (link). 

epsilon: float that will be used to replace a zero in the product of the conditional probabilites. This should be tweaked depending on
			the other inputs since it can cause the most issues. The goal is to make the epsilon small enough that it makes the 
			probability less significant than the acutal strongest related page, but not too weak to zero out the number with a 
			floating point error.

***OUTPUT***
distributions: a list of tuples where the first value in the tuple is the category and the second value is 
				probability that the given page belongs to that category. 

"""
def naiveBayes(classPage,allCatsLinks,occurMatrix,totals,keyDict,epsilon=1e-1):
	distribution = [1]*len(allCatsLinks)
	for link in classPage.links:
		for i in xrange(len(allCatsLinks)):
			if link in keyDict:
				index = keyDict[link]
				val = occurMatrix[i][index]
				tot = totals[index]
				liklihood = val/float(tot)
				if liklihood == 0:
					distribution[i] *= epsilon
				else:
					distribution[i] *= liklihood
			else:
				distribution[i] *= epsilon
	new_dist = normalize(distribution)
	return [(allCatsLinks[i],new_dist[i]) for i in range(len(allCatsLinks))]


def normalize(vector):
	total = sum(vector)
	new = [float(i)/total for i in vector]
	return new 




