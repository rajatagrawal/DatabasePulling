import urllib2
import re
from binaryTree import tree


stopWordsTree = tree()
searchStringsTree = tree()

print 'Starting Indexing'
urlFile = open('./reviewUrls.txt')
urls = urlFile.readlines()
counter = 0;
def addStopWords():
	stopWordFile = open('./stopWords.txt')
	stopWords = stopWordFile.readlines();
	for stopWord in stopWords:
		stopWordsTree.addNode(stopWord.lower().strip());
addStopWords();
print 'Finished Hashing Stop Words';
def consumeAURL(urlToFetch):
		try:
			global counter;
			urlFile = urllib2.urlopen(urlToFetch)
			
			counter = counter + 1;
			print 'Started Indexing url number ' + str(counter)
		except:
			#global counter;
			print ' Did not get the url ' + str(counter) + ' because of HTTP Error or URL Error'
			return;
		fileData = urlFile.readlines()
		shoeBrand = fileData[0];
		shoeBrand = shoeBrand.lower().strip()
		fileData = fileData[1:]
			

		#parse the reviews
		for line in fileData:
			selectedWords = []
			reviewWords = re.split('\W+',line)
			reviewWords = [word.lower() for word in reviewWords]
			for word in reviewWords:
				if stopWordsTree.search(word) == False:
					if word not in selectedWords:
						selectedWords.append(word)
			#print 'The original words were ' + str(reviewWords);
			#print 'Selected Words are ' + str(selectedWords);
			for word in selectedWords:
				searchStringsTree.addIndex(word,shoeBrand);		
for url in urls[0:1]:
	consumeAURL(url.strip());

userInput =''
while userInput.lower() != 'exit':
	userInput = raw_input('Enter a search string to search for reviews : ')
	userInput = userInput.lower()
	searchStringsTree.searchAndPrintReviews(userInput);
