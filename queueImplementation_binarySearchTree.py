import Queue
import threading
import urllib2
import re
from binaryTree import tree


workQueue = Queue.Queue()
workLock = threading.Lock()
stopWordsTree = tree()
searchStringsTree = tree()

print 'Starting Indexing'
urlFile = open('./reviewUrls.txt')
urls = urlFile.readlines()
def addURLs():
	for url in urls:
		workQueue.put(url.strip())
	#workQueue.join()
producerThread = threading.Thread(target = addURLs);
producerThread.start();
producerThread.join();
print 'The size of urls is ' + str(workQueue.qsize())
counter = 0;
def addStopWords():
	stopWordFile = open('./stopWords.txt')
	stopWords = stopWordFile.readlines();
	for stopWord in stopWords:
		stopWordsTree.addNode(stopWord.lower().strip());
addStopWords();
print 'Finished Hashing Stop Words';
def consumeAURL():
	while workQueue.empty() == False:
		urlToFetch = workQueue.get()
		#print 'URL To fetch is ' + urlToFetch
		try:
			global counter;
			urlFile = urllib2.urlopen(urlToFetch)
			
			workLock.acquire();
			counter = counter + 1;
			workLock.release();
			print 'Started Indexing url number ' + str(counter)
		except:
			#global counter;
			workLock.acquire();
			print ' Did not get the url ' + str(counter) + ' because of HTTP Error or URL Error'
			workLock.release()
			continue;
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
			workLock.acquire();
			for word in selectedWords:
				searchStringsTree.addIndex(word,shoeBrand);		
				#if word not in searchStringsHashTable:
				#	searchStringsHashTable[word] = []
				#	searchStringsHashTable[word] = searchStringsHashTable[word] + [[shoeBrand,1]]
					#print word + ' : ' + str(searchStringsHashTable[word]);
				#else:
				#	shoeList = searchStringsHashTable[word]
				#	shoeAdded = False;
				#	for i in range(len(shoeList)):
				#		if shoeList[i][0] == shoeBrand:
				#			shoeList[i][1] = shoeList[i][1] + 1
				#			shoeAdded = True;
				#			break;
				#	if shoeAdded == False:
				#		shoeList = shoeList + [[shoeBrand,1]]
				#	searchStringsHashTable[word] = shoeList;
					#print  word + ' : ' + str(searchStringsHashTable[word])
			workLock.release()			
numberOfThreads = 500;
for i in range(numberOfThreads):
	consumerThread = threading.Thread(target=consumeAURL);
	consumerThread.start()
	consumerThread.join()

print 'All files have been fetched and URL processing queue size is ' + str(workQueue.qsize())
userInput =''
while userInput.lower() != 'exit':
	userInput = raw_input('Enter a search string to search for reviews : ')
	userInput = userInput.lower()
	searchStringsTree.searchAndPrintReviews(userInput);
		#for shoeReview in searchStringsHashTable[userInput]:
		#	print 'Found in ' + str(shoeReview[1]) +  ' reviews for ' + shoeReview[0]
	#else:
	#	print 'Sorry the search string entered is not in the reviews'
