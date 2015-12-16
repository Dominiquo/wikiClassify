import categories
import page
from bs4 import BeautifulSoup
import page
import requests
import sqlite3
import unicodedata
import sys

"""
Creating a 

"""
def createClassifier(categoriesLinks,max_depth=1):
	allCategories = []
	allCatsLinks = []
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

	return allCatsLinks,occurMatrix,totals,keyDict


def naiveBayes(classPage,allCatsLinks,occurMatrix,totals,keyDict,epsilon=1e-2):
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




