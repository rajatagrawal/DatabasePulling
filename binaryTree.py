class node:
	def __init__(self):
		self.value = "";
		self.left = None;
		self.right = None;
		self.reviewList = []

class tree:
	def __init__(self):
		self.root = None;

	def addNode(self,nodeString):
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
	
	def addIndex(self,nodeString,shoeBrand):
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
			if nodeString < parent.value:
				parent.left = node();
				parent.left.value = nodeString;
				parent.left.reviewList.append([shoeBrand,1]);
			else:
				parent.right = node();
				parent.right.value = nodeString;
				parent.right.reviewList.append([shoeBrand,1]);
		return True;

	def doInorder(self,node):
		if node == None:
			return;
		self.doInorder(node.left);
		print 'node is ' + node.value + ' and review list is ' + str(node.reviewList);
		self.doInorder(node.right);
	
	def doIndex(self,nodeString,shoeBrand):
		temp = self.root;
		while temp != None:
			if temp.value == nodeString:
				for i in range(len(reviewList)):
					if shoeBrand == reviewList[i][0]:
						reviewList[i][1] = reviewList[i][1] + 1;
				reviewList.append([shoeBrand,1]);
				return True;
			elif nodeString< temp.value:
				temp = temp.left;
			elif nodeString>temp.value:
				temp = temp.right;
		return False;


	def search(self,nodeString):
		temp = self.root;
		while temp != None:
			if temp.value == nodeString:
				return True;
			elif nodeString< temp.value:
				temp = temp.left;
			elif nodeString>temp.value:
				temp = temp.right;
		return False;
	def searchAndPrintReviews(self,nodeString):
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
