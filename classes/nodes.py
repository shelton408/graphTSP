class basicNode:
	nodeType = ""
	neighbors = []
	x = 0
	y = 0
	def __init__(self, nodeT):
		self.nodeType = nodeT
		self.neighbors = []
	def __repr__(self):
		return str((self.getT(),self.getCoord()))
	def __str__(self):
		return self.getT()
	#get/set funcs
	def addNeighbor(self, node, dist):
		self.neighbors.append((node,dist))
	def getNeighbors(self):
		return self.neighbors
	def setX(self, X):
		self.x = X
	def setY(self, Y):
		self.y = Y
	def getCoord(self):
		return (self.x,self.y)
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getT(self):
		return self.nodeType
	def equals(self, node):
		return ((self.getX()==node.get()) and (self.getY()==node.getY()))
