import urllib2
import threading
import re
from binaryTree import tree

#read the url files and store the name of file address in a local variable
#and download them in a directory on the filesystem

resourceFile = open('./reviewURLs.txt');
urls = resourceFile.readlines();

indexTree = tree();
ignoreWords = tree();

ignoreIndexFile = open('./stopWords.txt');
stopWords = ignoreIndexFile.readlines();
for word in stopWords:
	ignoreWords.addNode(word.lower().strip());


#this function downloads a file from a url specified in the url list file.
def readAResourceFile(inputURL):
	inputFile = urllib2.urlopen(inputURL);
	fileData = inputFile.readlines();
	#shoeBrand = fileData[0];
	#fileData = fileData[1:];
	#for line in fileData:
	#	selectedWords = []
	#	words = re.split("\W+",line);
	#	words = [lowerCaseWord.lower() for lowerCaseWord in words]
	#	for word in words:
	#		if ignoreWords.search(word)== False:
	#			try:
	#				if selectedWords.index(word):
	#					continue;
	#			except ValueError:
	#				selectedWords.append(word);
	#	for word in selectedWords:
	#		indexTree.addIndex(word,shoeBrand.lower().strip());
# this for loop below calls the readAResourceFile function for every file in the urllist file in a new thread.
# hence every file in the urllist is downloaded and stored on the file system in a new thread.

urls = [urlLine.strip() for urlLine in urls]
print 'Number of urls to index is ' + str (len(urls));
print 'Indexing the data...';
for url in urls:
	thread = threading.Thread(target = readAResourceFile,args=(url,));
	thread.start();

print 'Indexing is done'
userString = ''
while userString.lower() != 'exit':
	userString = raw_input("Enter a String to search : ")
	indexTree.searchAndPrintReviews(userString.lower());
