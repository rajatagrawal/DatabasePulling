import urllib2
import re
stopWordsHashTable = {}
searchStringsHashTable = {}
print 'Starting Indexing'
urlFile = open('./reviewUrls.txt')
urls = urlFile.readlines()
print 'The size of urls is ' + str(len(urls))
counter = 0;
def addStopWords():
	stopWordFile = open('./stopWords.txt')
	stopWords = stopWordFile.readlines();
	for stopWord in stopWords:
		stopWordsHashTable[stopWord.lower().strip()] = 0;
addStopWords();
print 'Finished Hashing Stop Words';
def consumeAURL(urlToFetch):
		try:
			global counter;
			urlFile = urllib2.urlopen(urlToFetch)
			counter = counter + 1;
			print 'Started Indexing url number ' + str(counter)
		except:
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
				if word not in stopWordsHashTable:
					if word not in selectedWords:
						selectedWords.append(word)
			#print 'The original words were ' + str(reviewWords);
			#print 'Selected Words are ' + str(selectedWords);
			for word in selectedWords:
				if word not in searchStringsHashTable:
					searchStringsHashTable[word] = []
					searchStringsHashTable[word] = searchStringsHashTable[word] + [[shoeBrand,1]]
					#print word + ' : ' + str(searchStringsHashTable[word]);
				else:
					shoeList = searchStringsHashTable[word]
					shoeAdded = False;
					for i in range(len(shoeList)):
						if shoeList[i][0] == shoeBrand:
							shoeList[i][1] = shoeList[i][1] + 1
							shoeAdded = True;
							break;
					if shoeAdded == False:
						shoeList = shoeList + [[shoeBrand,1]]
					searchStringsHashTable[word] = shoeList;
					#print  word + ' : ' + str(searchStringsHashTable[word])
for url in urls:
	consumeAURL(url.strip());

#print 'All files have been fetched and URL processing queue size is ' + str(workQueue.qsize())
userInput =''
while userInput.lower() != 'exit':
	userInput = raw_input('Enter a search string to search for reviews : ')
	userInput = userInput.lower()
	if userInput in searchStringsHashTable:
		for shoeReview in searchStringsHashTable[userInput]:
			print 'Found in ' + str(shoeReview[1]) +  ' reviews for ' + shoeReview[0]
	else:
		print 'Sorry the search string entered is not in the reviews'
