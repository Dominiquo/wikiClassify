# wikiClassify

The goal of this project is to find the distribution of how likely a page is to belong to some given Wikipedia categories.

### Requirements
- BeautifulSoup 4
- NLTK Corpus
- Python 2.7.10 (requests creates an SSL error with earlier versions)

### Main

To run the classifier, run the main method in the terminal. This will ask a series of questions and take your input to build the model.
It is important to enter the link suffixes and not the entire links. Also, depth 1 is my recommended depth because it could take a very long
time to collect the data at further depths. If you say that you have already calculated prior probabilites, the method will use the default 
model which is trained on the following categories.

- http://en.wikipedia.org/wiki/Category:Rare_diseases
- http://en.wikipedia.org/wiki/Category:Infectious_diseases
- http://en.wikipedia.org/wiki/Category:Cancer
- http://en.wikipedia.org/wiki/Category:Congenital_disorders
- http://en.wikipedia.org/wiki/Category:Organs_(anatomy)
- http://en.wikipedia.org/wiki/Category:Machine_learning_algorithms
- http://en.wikipedia.org/wiki/Category:Medical_devices

This will skip you forward to just giving a page which will classify relatively quickly.

### Classifier

I decided to use a naive bayes classifier because I believed I would get the 'most bang for my buck' without using any external libraries.
I wanted something that would could be done completely rather than reaching for something more complicated and not be able to raise it to
my own satisfaction. I found it to be more important to have something that works okay than something that could work well if the kinks were fixed.
I definitely know this is far from perfect, and I plan on revising this later to include different classifiers that use libraries and 
therefore more complexity without the time of using pure python code. </br>
With my initial 'createClassifier' method, I recurse through the categories and store all words (or links) and their count. I use a map to
store the index of each word (or link) in this matrix that way when I check later, I use this as my mapping. I also maintain the list
of categories so I know which row relates to which category later when I am calculating the probabilites. </br>

###Thoughts while Making Classifer

I went through several iterations of trying to figure out the best way to use the given pages to extract features. I initially wanted to 
use my approach of extracting all links from a page because I felt this would really get the essence of what a page meant without getting
too much data from a page. I think this may have been too specific, so I added on the option to classify with words even though I had 
already made the functionality to scrape the words, I didn't think it would be used immediately. When I went to using words, I then realized
that there are many filler words that may be scewing the probabilities unfairly on the number of subdocuments that lie in a categories range.
For example, rare diseases has many more subpages than organs and therefore the word cound of articles and other stop words would be 
unfairly higher. To counter this, I just filtered stop words altogether, but I still think this difference in size is a pretty big issue
for the naive bayes classifier that I didn't realize until after. Also, numerical rounding issues became a problem, which I shouldn've 
expected. Since I wanted to return the full distribution and not just the argmax of which category the article belongs to, I couldn't
do the normal addition of logs of probabilities, so I just renormalized the vector after every iteration. This doesn't hurt the runtime too
badly as long as the number of categories is relatively small as I have in this example, but either way, it's just a numerical operation and 
not fetching data from a website. 

###Structure of Scraper

When creating this, I immediately saw the recursive structure of the categories and each category contains subpages and subcategories. This
was my motive for creating a page type and categories type (in hindsight, it should just be category, but that's not important). I also 
realized very quickly, that the number of pages related to a category grows very quickly. I initially wanted to scrape until the number of 
subcategories for a subcategories went to zero and only subpages remained making that category a leaf in this tree, but I realized this 
meant that I would have to visit hundreds of thousands of pages, and these pages may veer far from the essence of the original category. </br>
For each Categories type, I can get the subpages and subcategores, and get all leaf pages at a given depth. What this method does is recurse
on each sub category and calls this method on them adding all their subpages to the root's list of subpages. I also thought it was important
to store the depth as a field of the page. Perhaps in later classification, we can way a pages features less since it is further from the root,
but I have yet to use that currently.</br>
Each page type stores the depth as I said earlier along with a dictionary of word occurences and a list of page links. I decided to store
these links as strings rather than page types, because this would basically become a crawler of I collected all outgoing pages of a page 
and kept doing this. As I stated earlier, I decided to filter out stop words from pages becaues this seemed logical as the words aren't
too relevant to the content of the page. 

###Results
I am not fully satisfied with the results for the given categories, but that leads me to believe this problem will require a more
sophisticated classifier. I also noticed that most of the probabilities tend to zero for all of the categories except the chosen category.
I feel this may have something to do with my choice of epsilon, but also it may be inherent to naive bayes itself. I examined some of the
matching words between files for something that was categorized wrong ('/wiki/Cancer_and_nausea') and realized that words I expected to 
have a closer match with the cancer category did, but too many others matched with categories like infectious diseases. I believe the sheer
size of the words that occured in things like rare diseases really throws off the classifier. Also, when examining this I realized I was looking
for 'key words' that I expected to show up in Cancer topics and weighing these higher in my mind. Naive Bayes doesn't do this. This is a 
huge problem with classifer itself--it ignores all structure and importance of words in a paper. When checking a Machine Learning page on 
the classifier, this worked very well because it obviously is almost mutually exclusive from the other categories. I expected this. Given new
pages, I think Naive bayes was ultimately a poor choice. The random page may have some collisions with important words that are rightly
classifying the page, but I think most of the time those will be outweighed by the coincidence and mass of some categories.

###Additions
Without completely making a new classifier, I think a possibility is creating some type of n-gram dictionary for the paper. This would let
me continue to use Naive Bayes while adding some structure to the results. Outside of that, I am going to look into some methods of 
normalizing the categories with each other so I am not facing this issue of having some contribute much more words than others.

###running outside of terminal
I personally never really ran the program because using sublime, it was easier to just change my code in other methods and run directly from there.
To do this, use the generatePriorOnGivenWikiCategories function and checkPage function. I have documented these with comments pretty 
thoroughly, so it should make sense in the code. I highly recommend looking at the actual code if anything isn't going as desired or you
would like to tweak it for yourself. I have tried my best to make the code as readable and provide thorough comments. 



