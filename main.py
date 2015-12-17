import categories
import page
import classify
import pickle


def generatePriorOnGivenWikiCategories(depth=1,links=True):
	rareDisLink = '/wiki/Category:Rare_diseases'
	infecDisLink = '/wiki/Category:Infectious_diseases'
	cancerLink = '/wiki/Category:Cancer'
	congenitialDis = '/wiki/Category:Congenital_disorders'
	organsLink = '/wiki/Category:Organs_(anatomy)'
	MLLinks = '/wiki/Category:Machine_learning_algorithms'
	medDevLinks = '/wiki/Category:Medical_devices'
	catLinks = [rareDisLink,infecDisLink,cancerLink,congenitialDis,organsLink,MLLinks,medDevLinks]
	# catLinks = [cancerLink,organsLink] #a smaller subset of the links if I want to test the algorithm for higher depths
	print 'getting prior probabilities for the given categories...'
	allCatsLinks,occurMatrix,totals,keyDict,useLinks = classify.createClassifier(catLinks,links,depth)

	serialize(allCatsLinks,'allCatsLinks.p')
	serialize(occurMatrix,'occurMatrix.p')
	serialize(totals,'totals.p')
	serialize(keyDict,'keyDict.p')
	serialize(useLinks,'useLinks.p')

	print "prior probabilites have been serialized for depth =",depth

	return None	

def checkPage(link):
	checkPage = page.Page(link)

	print 'Getting distribution for page over categories...'
	allCatsLinks = unpack('allCatsLinks.p')
	occurMatrix = unpack('occurMatrix.p')
	totals = unpack('totals.p')
	keyDict = unpack('keyDict.p')
	useLinks = unpack('useLinks.p')
	distribution = classify.naiveBayes(checkPage,allCatsLinks,occurMatrix,totals,keyDict,useLinks)
	for result in distribution:
		print link,'is a subpage of', result[0], 'with probability', round(result[1]*100,5),'%'

	return None


def serialize(obj,filename):
	try:
		pickle.dump(obj,open(filename,'wb'))
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return False
	return True

def unpack(filename):
	try:
		return pickle.load(open(filename,"rb"))
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return False

def main():
	already_made = False
	while True:
		made = raw_input("Have you already initialized a prior probability?(Y/N) ")
		if made == "Y":
			already_made = True
			break
		elif made == "N":
			already_made = False
			break

	if not already_made:
		while True:
			catCount = raw_input("How many categories will you be using? ")
			try:
				count = int(catCount)
				break
			except:
				print "not a valid integer"

		while True:
			inpDepth = raw_input("How deep do you want to traverse (increases exponentially)? ")
			try:
				depth = int(inpDepth)
				break
			except:
				print "not a valid integer"

		while True:
			bagOfWords = raw_input("Use link approach or bag of words?(enter 1/0 respectively): ")
			try:
				BOWval = int(bagOfWords)
				useLinks = not not BOWval
				break
			except:
				print "not a valid integer"

		allCategoriesLinks = []
		print 'Please give the input in the form \"/wiki/Category:Example_category\".'
		print 'If a category is not valid input or not recognized, it will be dropped by the classifier.'
		for i in xrange(int(catCount)):
			catLink = raw_input("enter your category: ")
			allCategoriesLinks.append(catLink)

		print 'Creating prior probilities for naive bayes clssification...'
		allCatsLinks,occurMatrix,totals,keyDict,useLinks = classify.createClassifier(allCategoriesLinks,useLinks,depth)

		serialize(allCatsLinks,'allCatsLinks.p')
		serialize(occurMatrix,'occurMatrix.p')
		serialize(totals,'totals.p')
		serialize(keyDict,'keyDict.p')
		serialize(useLinks,'useLinks.p')
		print 'Prior probabilities are now stored in serialized files.'

	while True:
		checkPageLink = raw_input("In similar format, give URL suffix of page you would like to classify: ")
		if page.isPage(checkPageLink):
			break
		else:
			print "There was an error connecting to the given page."

	checkPage = page.Page(checkPageLink)

	print 'Getting distribution for page over categories...'
	allCatsLinks = unpack('allCatsLinks.p')
	occurMatrix = unpack('occurMatrix.p')
	totals = unpack('totals.p')
	keyDict = unpack('keyDict.p')
	useLinks = unpack('useLinks.p')
	distribution = classify.naiveBayes(checkPage,allCatsLinks,occurMatrix,totals,keyDict,useLinks)
	for result in distribution:
		print checkPageLink,'is a subpage of', result[0], 'with probability', round(result[1]*100,5),'%'

	return None


if __name__ == "__main__":
	main()
	# generatePriorOnGivenWikiCategories(1,False)
	KernelMethod = '/wiki/Kernel_methods_for_vector_output' #pulled from machine learning topics
	tobacco = '/wiki/Tobacco' #pulled from cancer
	neonatal = '/wiki/Neonatal_sepsis' #pulled from infectious diseases
	syphilis = '/wiki/Congenital_syphilis' #pulled from infectious diseases
	kuru = '/wiki/Kuru_(disease)' #rare diseases
	DIX = '/wiki/DIXDC1' #cancer
	nausea = '/wiki/Cancer_and_nausea'
	# checkPage(tobacco)

