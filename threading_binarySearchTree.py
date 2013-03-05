import Queue
import threading
import urllib2
import re
from binaryTree import tree

#this is the work queue that holds the urls that need to be processed
workQueue = Queue.Queue()

#this is a lock that is used to do synchronization when multiple threads are trying to access the hash table
workLock = threading.Lock()

#this is the binary search tree that will index the words that need to be ignored while indexing the search strings
stopWordsTree = tree()

#this is the binary search tree that will index the search strings
searchStringsTree = tree()

print 'Starting Indexing'

#open the file containing the list of urls and load them in the memory
urlFile = open('./reviewUrls.txt')
urls = urlFile.readlines()

#this function puts the urls that are read from the file in the work queue that was defined earlier
def addURLs():
	for url in urls:
		workQueue.put(url.strip())
	#workQueue.join()

#a separate thread is created to put all the urls read from the url's file into the queue. This thread executes the addURLs function
producerThread = threading.Thread(target = addURLs);
producerThread.start();
producerThread.join();

#prints the number of urls that need to be processed by printing the number of urls present in the queue
print 'The size of urls is ' + str(workQueue.qsize())
counter = 0;

#this function hashes the words that need to be ignored while indexing search words.
#this function reads every word present in the stopWords.txt file and hashes them in the hash table defined above

def addStopWords():
	stopWordFile = open('./stopWords.txt')
	stopWords = stopWordFile.readlines();
	for stopWord in stopWords:
		stopWordsTree.addNode(stopWord.lower().strip());

addStopWords();
print 'Finished Hashing Stop Words';

#this function does the processing for a single url
def consumeAURL():
    
    #while there are more urls in the work queue present to be processed, dequeue a url
	while workQueue.empty() == False:
		urlToFetch = workQueue.get()
		#print 'URL To fetch is ' + urlToFetch

        	#try opening the url
        	try:
			global counter;
			urlFile = urllib2.urlopen(urlToFetch)
			
			workLock.acquire();
			counter = counter + 1;
			workLock.release();
			print 'Started Indexing url number ' + str(counter)

        	#if the url cannot be opened, catch the exception and print an error message and ignore this url
        	except:
			#global counter;
			workLock.acquire();
			print ' Did not get the url ' + str(counter) + ' because of HTTP Error or URL Error'
			workLock.release()
			continue;
                
        	#read the contents of the file specified by the url
		fileData = urlFile.readlines()
                
        	#extract the shoebrand and the model from the first line of the contents of the review file
		shoeBrand = fileData[0];
		shoeBrand = shoeBrand.lower().strip()
                
        	#store the reviews in this file
		fileData = fileData[1:]
			

		#parse the reviews
		for line in fileData:
            
            		#stores the words that would be hashed into the hash table
			selectedWords = []
            
            		#split the lines into words by using non-alphanumberic characters as delimitters
			reviewWords = re.split('\W+',line)
            
            		#convert the words into lower case so that it is easier for comparison
			reviewWords = [word.lower() for word in reviewWords]
            
            		#for every word in each review
			for word in reviewWords:
                		# if the word is not in the tree that indexes the words that need to be ignored
				if stopWordsTree.search(word) == False:
                    
                    			# if the word has already not been selected for indexing. This is done to remove duplicacy for a word that is present multiple
					# times in a same review
					if word not in selectedWords:
						selectedWords.append(word)
            
			#print 'The original words were ' + str(reviewWords);
			#print 'Selected Words are ' + str(selectedWords);
                
                
            		# A locking mechanisim to acquire a lock to ensure that there is only one thread that is reading/writing/making modification to the hash table at a time
			workLock.acquire();
                
			for word in selectedWords:
                	
			#index each word in the list of selected Words. This funciton built by me takes care by itself if the word has been already indexed or if a word indexed in the tree exists in the review for a current shoe brand
				searchStringsTree.addIndex(word,shoeBrand);
                
            		#after the processing is done, release the lock
			workLock.release()

#initializing the number of threads that will process the data
numberOfThreads = 500;

#starting threads that will process the data
for i in range(numberOfThreads):
	consumerThread = threading.Thread(target=consumeAURL);
	consumerThread.start()
    
    #doing join so that the main program doesn't exit before any of the threads haven't finished processing the data
	consumerThread.join()

print 'All files have been fetched and URL processing queue size is ' + str(workQueue.qsize())
userInput =''

#taking input from the user to enter a search string
#unless the user enters a search string 'exit', the program asks the user to enter a search string
while userInput.lower() != 'exit':
	userInput = raw_input('Enter a search string to search for reviews : ')
	userInput = userInput.lower()
    
	#search for user input and output the result. The function built by me automatically takes care of a search that is present in the index tree and which are not present in the index tree.
	searchStringsTree.searchAndPrintReviews(userInput);
