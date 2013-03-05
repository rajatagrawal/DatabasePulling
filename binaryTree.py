class node:
	def __init__(self):
		self.value = "";
		self.left = None;
		self.right = None;
		self.reviewList = []

class tree:
	def __init__(self):
		self.root = None;

	#add a new node to the binary tree. Used for a stop word node to the index tree for stop words
	def addNode(self,nodeString):
		nodeString = nodeString.lower()
		if self.root == None:
			self.root = node()
			self.root.value = nodeString
		else:
			parent = None;
			temp = self.root;
			while temp != None:
				if nodeString<temp.value:
					parent = temp;
					temp = temp.left;
				elif nodeString>temp.value:
					parent = temp;
					temp = temp.right;
				else:
					return False;
			if nodeString < parent.value:
				parent.left = node();
				parent.left.value = nodeString;
			else:
				parent.right = node();
				parent.right.value = nodeString;
		return True;
	
	# adds an index for the search string to the searchStrings index tree
	def addIndex(self,nodeString,shoeBrand):
		nodeString = nodeString.lower()
		shoeBrand = shoeBrand.lower()
		if self.root == None:
			self.root = node()
			self.root.value = nodeString
			self.root.reviewList.append([shoeBrand,1]);			
		else:
			parent = None;
			temp = self.root;
			while temp != None:
				if nodeString<temp.value:
					parent = temp;
					temp = temp.left;
				elif nodeString>temp.value:
					parent = temp;
					temp = temp.right;
				elif nodeString == temp.value:
					for i in range(len(temp.reviewList)):
						if shoeBrand == temp.reviewList[i][0]:
							temp.reviewList[i][1] = temp.reviewList[i][1] + 1;
							return True;
					temp.reviewList.append([shoeBrand,1]);
					return True;
			if nodeString < parent.value:
				parent.left = node();
				parent.left.value = nodeString;
				parent.left.reviewList.append([shoeBrand,1]);
			else:
				parent.right = node();
				parent.right.value = nodeString;
				parent.right.reviewList.append([shoeBrand,1]);
		return True;

	#prints the binary tree
	def doInorder(self,node):
		if node == None:
			return;
		self.doInorder(node.left);
		print 'node is ' + node.value + ' and review list is ' + str(node.reviewList);
		self.doInorder(node.right);
	
	# searches for a node in a binary tree. Used to search for stop words in the stop word index tree
	def search(self,nodeString):
		nodeString.lower()
		temp = self.root;
		while temp != None:
			if temp.value == nodeString:
				return True;
			elif nodeString< temp.value:
				temp = temp.left;
			elif nodeString>temp.value:
				temp = temp.right;
		return False;

	# searches for a search string and prints the reviews attached for the search string. Used in the searchStrings index tree
	def searchAndPrintReviews(self,nodeString):
		nodeString.lower()
		temp = self.root;
		while temp != None:
			if temp.value == nodeString:
				for review in temp.reviewList:
					print 'Found in ' + str(review[1]) + ' reviews for ' + review[0];
				return True 
			elif nodeString< temp.value:
				temp = temp.left;
			elif nodeString>temp.value:
				temp = temp.right;
		print 'Sorry! There are no reviews with the given search string : ' + nodeString;
		return False;


#binaryTree = tree();
#binaryTree.addNode("abc");
#binaryTree.addNode("aaa");
#binaryTree.addNode("bbb");
#binaryTree.addNode("abc");
#binaryTree.addNode("aaa");
#binaryTree.doInorder(binaryTree.root);
#print binaryTree.search("abcdef");
