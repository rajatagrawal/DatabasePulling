DatabasePulling
===============

This is a python code that pulls out data from a list of urls and creates a search index for searching for a particular word in a review in O(1) time.

There are 2000 urls in a text file, reviewUrls.txt. Each url has some reviews. The seach indexing function creates a search index for the reviews in the urls so that all the reviews having a particular search word can be pulled in O(1) time.


There are four main files in the code.

1. singleThreading_binarySearchTree.py - Does the processing using a single thread and binary trees.
2. singleThreading_hashing.py - Does the search indexing using a single thread and a hash table.
3. threading_binarySearchTree.py - Does the processing using multiple threads and a binary search tree.
4. threading_hashTable.py - Does the processing using multiple threads and a hash table.

The order of time performance is 4>3>2>1 in the increasing order of time taken to index the reviews in the url.

The other files in the code are,

1. reviewUrls.txt : A file containing the urls from where to pull the data
2. binaryTree.py : A self implemented implementation for a binary tree for functionalities needed by me in the code
3. stopWords.txt : A list of common words that need to be ignored while creating a search index.
