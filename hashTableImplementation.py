import urllib2
import threading
import re
from binaryTree import tree
import Queue

#read the url files and store the name of file address in a local variable
#and download them in a directory on the filesystem

indexTree = tree();
ignoreWords = tree();

stopWordsHashTable = {}
searchStringHashTable = {}
hashTableLock = threading.Lock()
urlQueue = Queue.Queue();
numberOfThreads = 2081;

resourceFile = open('./reviewURLs.txt');
urls = resourceFile.readlines();
for url in urls:
	urlQueue.put(url.strip())

print 'The size of the queue is ' + str(urlQueue.qsize())
ignoreIndexFile = open('./stopWords.txt');
stopWords = ignoreIndexFile.readlines();
for word in stopWords:
	stopWordsHashTable[word.lower().strip()] = 0;
	#ignoreWords.addNode(word.lower().strip());

#this function downloads a file from a url specified in the url list file.
def readAResourceFile():
	inputURL = urlQueue.get()
	inputFile = urllib2.urlopen(inputURL);
	#inputFile = file(inputURL);
	fileData = inputFile.readlines();
	#inputFile.close()
	shoeBrand = fileData[0];
	shoeBrand = shoeBrand.lower().strip()
	fileData = fileData[1:];
	for line in fileData:
		selectedWords = []
		words = re.split("\W+",line);
		words = [lowerCaseWord.lower() for lowerCaseWord in words]
		for word in words:
			#if ignoreWords.search(word)== False:
			if word not in stopWordsHashTable:
				try:
					if selectedWords.index(word):
						continue;
				except ValueError:
					selectedWords.append(word);
		#hashTableLock.acquire();
		for word in selectedWords:
			hashTableLock.acquire();
			if word in searchStringHashTable:
				modifiedTheValue = False;
				for i in range(len(searchStringHashTable[word])):
					print 'started a new word'				
					if (searchStringHashTable[word])[i][0] == shoeBrand:
						(searchStringHashTable[word])[i][1] = (searchStringHashTable[word])[i][1] + 1
						modifiedTheValue = True;
						print '\nset the value';
						#break;
				if modifiedTheValue == False:
					print 'coming in false'
					searchStringHashTable[word] = searchStringHashTable[word] + [[shoeBrand,1]]	
			else:
				searchStringHashTable[word] = []
				searchStringHashTable[word] = searchStringHashTable[word] + [[shoeBrand,1]]
			hashTableLock.release();
			#indexTree.addIndex(word,shoeBrand.lower().strip());
		#hashTableLock.release()


# this for loop below calls the readAResourceFile function for every file in the urllist file in a new thread.
# hence every file in the urllist is downloaded and stored on the file system in a new thread.

#urls = [urlLine.strip() for urlLine in urls]
print 'The number of file to index is ' + str (len(urls));
print 'Indexing the data';
for threadIndex in range(numberOfThreads):
	#fileCounter = fileCounter + 1;
	fileProcessingThread = threading.Thread(target = readAResourceFile);
	fileProcessingThread.start();
	#fileProcessingThread.join();

print 'Indexing is done'
print 'the size of queue after processing ' + str(urlQueue.qsize());
userString = ''
while userString.lower() != 'exit':
	userString = raw_input("Enter a String to search : ")
	if userString.lower() in searchStringHashTable:
		for i in range(len(searchStringHashTable[userString.lower()])):
		
			print ' Found ' + str((searchStringHashTable[userString.lower()])[i][1]) + ' reviews for ' + (searchStringHashTable[userString.lower()])[i][0]
	else:
		print ' There are no reviews with this search string';
	#indexTree.searchAndPrintReviews(userString.lower());
