from classes import nodes
import numpy as np
from collections import deque


#parseFileToArray, and parseArrayToNode can be combined, but are left apart to allow for alternate use cases
#takes a filename as parameter, and parses each character into the array
#reads a file in as a 2d array of characters
def parseFileToArray(fName):
	with open(fName) as fp:
		parsed = []
		for line in fp:
			if("\n" in line):
				line = line[:-1]
			arr = []
			for character in line:
				arr.append(character)
			parsed.append(arr)
		print("Parsed Graph:\n")
		for i in range(0, len(parsed)):
			print(str(parsed[i])+"\n")
		return parsed
#changes an array of strings to an array of nodes
def parseArrayToNodeArr(arr):
	nodeArr = []
	h = len(arr)
	w = len(arr[0])

	for i in range(0, h):
		nodeArr.append([])
	for y in range(0, h):
		for x in range(0, w):
			node = nodes.basicNode(arr[y][x])
			node.setX(x)
			node.setY(y)
			nodeArr[y].append(node)
	return nodeArr
#gets the first index of a nodetype in the array
def getFirstIndexOf(nodeArr, nodeType):
	coord = (-1,-1)
	yC = -1
	for y in range(0, len(nodeArr)):
		if(nodeArr[y].count('S') ==1):
			yC = y
	xC = nodeArr[yC].index('S')
	print("Coordinates of S:"+str((xC,yC)))
	return (xC,yC)
#forms a table of distances with index [i,j] = dist between nodes i and j
def formDistTable(nodeArr):
	print("")
	print("Distance table: \n")
	table = []
	nodeInd= []
	#run BFS on each node
	for y in range(0, len(nodeArr)):
		for x in range(0,len(nodeArr[0])):
			if(nodeArr[y][x].getT()!='.'and nodeArr[y][x].getT()!='#'):
					nodeInd.append((x,y))
	sortedInd = sorted(nodeInd, key = lambda x:x[0])
	for ind in sortedInd:
		x = ind[0]
		y = ind[1]
		formNeighbors((x,y), nodeArr)
		s = sorted(nodeArr[y][x].getNeighbors(),key = lambda x: (x[0].getX(),x[0].getY()))
		table.append(s)

	#reformat table so S as first lines, G is last, so we can run the dp from s to g
	startInd = 0
	endInd = 0
	n = len(table)
	for i in range(0, n):
			if(str(table[0][i][0])=='S'):
				indS = i
	for i in range(0, n):
			if(str(table[0][i][0])=='G'):
				indG = i
	#following part moves values so that S and G are the beginning and end points of the table
	#move values relating to G to the end of the table
	for y in range(0, n):
		temp = table[y][indG]
		temp1 = table[y][n-1]
		table[y][indG] = temp1
		table[y][n-1] = temp
	for x in range(0, n):
		temp = table[indG][x]
		temp1 = table[n-1][x]
		table[indG][x]=temp1
		table[n-1][x]=temp
	#move values relating to S to the beginning of the table
	for y in range(0, n):
		temp = table[y][indS]
		temp1 = table[y][0]
		table[y][indS] = temp1
		table[y][0] = temp
	for x in range(0, n):
		temp = table[indS][x]
		temp1 = table[0][x]
		table[indS][x]=temp1
		table[0][x]=temp

	#set S and G dist = 0
	table[n-1][0]=(table[n-1][0][0],0)
	temp = []
	#change from a table of nodes to a table of distances
	for i in table:
		arr = []
		for j in i:
			arr.append(j[1])
		temp.append(arr)
	#print distances
	for i in temp:
		print(i)
	return temp
#given a node, form all of its neighbors using BFS(branches end upon reaching a checkpoint)
def formNeighbors(start, nodeArr):
	root = nodeArr[start[1]][start[0]]
	q = deque([root])
	nextLayer = []
	visited = [(root.getCoord())]
	visitedCheckpoints = [root]
	dist = 0
	#use BFS to construct graph
	while(len(q)>0 or len(nextLayer)>0):

		dist+=1
		#append right side to queue
		while(len(q)>0):
			if(len(nodeArr[0])>(q[0].getX()+1)):
				temp = nodeArr[q[0].getY()][q[0].getX()+1]
				if(temp.getT()!= '#' and visited.count(temp.getCoord())==0):
					if(temp.getT() == '.'):
						nextLayer.append(temp)
					else:
						nextLayer.append(temp)
						root.addNeighbor(temp, dist)
					visited.append(temp.getCoord())
			#append left side to queue
			if(0<(q[0].getX()-1)):
				temp = nodeArr[q[0].getY()][q[0].getX()-1]
				if(temp.getT()!= '#' and visited.count(temp.getCoord())==0):
					if(temp.getT() == '.'):
						nextLayer.append(temp)
					else:
						nextLayer.append(temp)
						root.addNeighbor(temp, dist)
					visited.append(temp.getCoord())
			#append top side to queue
			if(0<(q[0].getY()-1)):
				temp = nodeArr[q[0].getY()-1][q[0].getX()]
				if(temp.getT()!= '#' and visited.count(temp.getCoord())==0):
					if(temp.getT() == '.'):
						nextLayer.append(temp)
					else:
						nextLayer.append(temp)
						root.addNeighbor(temp, dist)
					visited.append(temp.getCoord())
			#append bottom side to queue
			if(len(nodeArr)>(q[0].getY()+1)):
				temp = nodeArr[q[0].getY()+1][q[0].getX()]
				if(temp.getT()!= '#' and visited.count(temp.getCoord())==0):
					if(temp.getT() == '.'):
						nextLayer.append(temp)
					else:
						nextLayer.append(temp)
						root.addNeighbor(temp, dist)
					visited.append(temp.getCoord())
			q.popleft().getCoord()
		q.extend(nextLayer)
		nextLayer = []
	root.addNeighbor(root, 0)
#run TSP on a distance table
def TSP(distances):
	n = len(distances)
	exp = 2**n
	g=[]
	for i in range(0,n):
		temp = [-1]*exp
		g.append(temp)
	startInd = 0
	endInd = 0
	for i in range(0,n):
		g[i][0] = distances[i][0]
	res = tspIter(0,exp-2, g, n, exp, distances)
	return res

	#Propogate values in the DP table
def tspIter(start, end, g, n, exp, distances):
	mask = -1
	maskedVal = -1
	res = -1
	if(g[start][end]!=-1):
		return g[start][end]
	else:
		for i in range(0,n):
			mask = exp-1 - 2**i
			maskedVal = end&mask
			if(maskedVal!=end):
				temp = distances[start][i] +tspIter(i,maskedVal,g,n,exp,distances)
				if(res == -1 or res>temp):
					res = temp
		g[start][end] = res
	return res

#returns -1 if: not rectangular graph, cannot reach G from S through all X, or does not contain S or G
#returns the shortest distance through all checkpoints from S to G otherwise
#WARNING: READS ANY NON S,G,X,. point as a block
#when accessing a point from the graph arrays, the first index correspondes to y and second to x
def TSPGraphDist(fp):
	arr = parseFileToArray(fp)

	#count the numbers of goals starts and checkpoints to check for invalid graphs
	numG = 0
	for i in range(0, len(arr)):
		numG += arr[i].count('G')
	print("Number of goals:"+str(numG))
	if(numG!=1):
		return -1

	numS = 0
	for i in range(0, len(arr)):
		numS += arr[i].count('S')
	print("Number of starts:"+str(numS))
	if(numS!=1):
		return -1
	#count the number of checkpoints to ensure we pass all of them later
	numCP = 0
	for i in range(0, len(arr)):
		numCP += arr[i].count('X')
	print("Number of checkpoints:"+str(numCP))

	#check that file is in a rectangular format, otyherwise we can just end here
	w = len(arr[0])
	for i in range(0, len(arr)):
		if(len(arr[i])!=w):
			return -1
	nodeArr = parseArrayToNodeArr(arr)
	sCoord = getFirstIndexOf(arr, 'S')
	gCoord = getFirstIndexOf(arr, 'G')
	distances = formDistTable(nodeArr)

	if (len(distances)!=numCP+2):
		return -1

	dist = TSP(distances)
	return dist




#test implementation of TSPGraph with samp.txt as input
def main():
	while(True):

		filename = input("Input a filename to run TSP on, use ./samp.txt for a sample test(enter quit to exit):\n")
		if(filename=='quit'):
			break
		print("The minimum distance from the start to goal through all checkpoints is: "+str(TSPGraphDist(filename)))
		print("\n#######################################################################################")

#run quickhull, the plot will plot points in the convex hull
if __name__== "__main__":
	main()