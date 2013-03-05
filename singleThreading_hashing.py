import urllib2
import re

# this is the hash table that hashes the words that need to be ignored
stopWordsHashTable = {}

# this is the hash table that hashes the actual search strings that are searched in the program for reviews
searchStringsHashTable = {}

print 'Starting Indexing'

#open the file containing the list of urls and load them in the memory
urlFile = open('./reviewUrls.txt')
urls = urlFile.readlines()

print 'The size of urls is ' + str(len(urls))
counter = 0;

#this function hashes the words that need to be ignored while indexing search words.
#this function reads every word present in the stopWords.txt file and hashes them in the hash table defined above
def addStopWords():
	stopWordFile = open('./stopWords.txt')
	stopWords = stopWordFile.readlines();
	for stopWord in stopWords:
		stopWordsHashTable[stopWord.lower().strip()] = 0;

addStopWords();
print 'Finished Hashing Stop Words';

#this function does the processing for a single url
def consumeAURL(urlToFetch):
        	#try opening the url
		try:
			global counter;
			urlFile = urllib2.urlopen(urlToFetch)
			counter = counter + 1;
			print 'Started Indexing url number ' + str(counter)
    
        	#if the url cannot be opened, catch the exception and print an error message and ignore this url
		except:
			print ' Did not get the url ' + str(counter) + ' because of HTTP Error or URL Error'
            
            		#don't process the url if it can't be accessed
			return;

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
                		# if the word is not in the hash table that hashes the words that need to be ignored
				if word not in stopWordsHashTable:
                    
                    			# if the word has already not been selected for indexing. This is done to remove duplicacy for a word that is present multiple
					# times in a same review
					if word not in selectedWords:
						selectedWords.append(word)

			#print 'The original words were ' + str(reviewWords);
			#print 'Selected Words are ' + str(selectedWords);
                            
            		# for every word that is in the list of selected words
			for word in selectedWords:
                
                		#if the word has not been hashed before, hash it in the hash table
				if word not in searchStringsHashTable:
					searchStringsHashTable[word] = []
					searchStringsHashTable[word] = searchStringsHashTable[word] + [[shoeBrand,1]]
					#print word + ' : ' + str(searchStringsHashTable[word]);
                
                		# if the word has been already hashed before, find it has been found in a review for the current shoebrand
				else:
					shoeList = searchStringsHashTable[word]
					shoeAdded = False;
					for i in range(len(shoeList)):
                        
                        			# if theword has been in a review for the current shoe brand, increment the number of reviews counter for that shoebrand by 1
						if shoeList[i][0] == shoeBrand:
							shoeList[i][1] = shoeList[i][1] + 1
							shoeAdded = True;
							break;

                    			# if the word has not been found in a review for the current shoe brand, add a new node with current shoebrand and number of reviews initialized to 1
					if shoeAdded == False:
						shoeList = shoeList + [[shoeBrand,1]]
					searchStringsHashTable[word] = shoeList;
					#print  word + ' : ' + str(searchStringsHashTable[word])

#start processing the urls that read from the file
for url in urls:
	consumeAURL(url.strip());

#print 'All files have been fetched and URL processing queue size is ' + str(workQueue.qsize())
userInput =''

#taking input from the user to enter a search string
#unless the user enters a search string 'exit', the program asks the user to enter a search string
while userInput.lower() != 'exit':
	userInput = raw_input('Enter a search string to search for reviews : ')
	userInput = userInput.lower()
    
    	#search the hash table for search string entered by the user. If the search string is in hash table, print all the shoebrand and number of reviews for each shoe brand associated with search string
	if userInput in searchStringsHashTable:
		for shoeReview in searchStringsHashTable[userInput]:
			print 'Found in ' + str(shoeReview[1]) +  ' reviews for ' + shoeReview[0]
    	#else the search string is not present in the hash table
	else:
		print 'Sorry the search string entered is not in the reviews'
