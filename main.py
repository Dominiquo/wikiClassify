import categories
import page
import classify
import pickle



def tester():
	rareDisLink = '/wiki/Category:Rare_diseases'
	infecDisLink = '/wiki/Category:Infectious_diseases'
	cancerLink = '/wiki/Category:Cancer'
	congenitialDis = '/wiki/Category:Congenital_disorders'
	organsLink = '/wiki/Category:Organs_(anatomy)'
	MLLinks = '/wiki/Category:Machine_learning_algorithms'
	medDevLinks = '/wiki/Category:Medical_devices'

	checkPageLink = '/wiki/Kernel_methods_for_vector_output'
	checkPage = page.Page(checkPageLink)


	catLinks = [rareDisLink,infecDisLink,cancerLink,congenitialDis,organsLink,MLLinks,medDevLinks]
	print 'getting prior probabilities for the given categories...'
	allCatsLinks,occurMatrix,totals,keyDict = classify.createClassifier(catLinks)

	serialize(allCatsLinks,'allCatsLinks.p')
	serialize(occurMatrix,'occurMatrix.p')
	serialize(totals,'totals.p')
	serialize(keyDict,'keyDict.p')

	for result in classify.naiveBayes(checkPage,allCatsLinks,occurMatrix,totals,keyDict):
		print checkPageLink,'is a subpage of', result[0], 'with probability', round(result[1]*100,5),'%'

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
		catCount = raw_input("How many categories will you be using? ")
		allCategoriesLinks = []
		print 'Please give the input in the form \"/wiki/example_page\".'
		print 'If a category is not valid input or not recognized, it will be dropped by the classifier.'
		for i in xrange(int(catCount)):
			catLink = raw_input("enter your category: ")
			allCategoriesLinks.append(catLink)

		print 'Creating prior probilities for naive bayes clssification...'
		allCatsLinks,occurMatrix,totals,keyDict = classify.createClassifier(allCategoriesLinks)

		serialize(allCatsLinks,'allCatsLinks.p')
		serialize(occurMatrix,'occurMatrix.p')
		serialize(totals,'totals.p')
		serialize(keyDict,'keyDict.p')
		print 'Prior probabilities are now stored in serialized files.'

	while True:
		checkPageLink = raw_input("In same format, give URL suffix of page you would like to classify: ")
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
	distribution = classify.naiveBayes(checkPage,allCatsLinks,occurMatrix,totals,keyDict)
	for result in distribution:
		print checkPageLink,'is a subpage of', result[0], 'with probability', round(result[1]*100,5),'%'

	return None


if __name__ == "__main__":
	# main()
	tester()