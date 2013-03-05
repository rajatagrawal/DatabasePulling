DatabasePulling
===============

This is a python code that pulls out data from a list of urls and creates a search index for searching for a particular word in a review in O(1) time.

There are four main files in the code.

1. singleThreading_binarySearchTree.py - Does the processing using a single thread and binary trees.
2. singleThreading_hashing.py - Does the search indexing using a single thread and a hash table.
3. threading_binarySearchTree.py - Does the processing using multiple threads and a binary search tree.
4. threading_hashTable.py - Does the processing using multiple threads and a hash table.

The order of time performance is 4>3>2>1 in the increasing order of time taken to index the reviews in the url.
