# Cellular Automata for embryonic architecture modelling.



import random
import Tkinter


class ca:


	def __init__(self,d,n,death,div):
		self.space=[[0 for y in range(d)]  for x in range(d)]
		#self.step()
		self.n=n
		self.d=d
		self.functions= range(n+1)
		self.deathProb=death #threshold for random selection
		self.divProb=div
		self.app=(1,[1,2,3,4,5])
		##Update Method##
		#0-  asynchronously Consecutive
		#1 - asynchronously random
		#2 - synchronously
		self.updateMode=1
		self.choice=0 
		#division selection method
		#0 - random
		#1 - weighted
		#2 - inductive 		


	def step(self):
		#step the CA by 
		if self.updateMode==0:     #async Consecutive		#broken
			for  y in range(self.d):
				for x in range(self.d):
					self.states(y,x,self.space)
		elif self.updateMode==1:	#async randomly			
			ch=[]
			for y in range(self.d):
				ch=ch+[(y,x) for x in range(self.d)]
			random.shuffle(ch)
			for y in ch:
				self.states(y[0],y[1],self.space)
		elif self.updateMode==2:	#sync
			tempMap=[[0 for y in range(self.d)]  for x in range(self.d)]
			for y in range(self.d):
				for x in range(self.d):
					tempMap[y][x]=self.space[y][x]
			for y in range(self.d):
				for x in range(self.d):
					self.states(y,x,tempMap)


	def printSpace(self):
		for y in self.space:
			print y

	def run(self,steps):
		#execute CA
		pass

	def getInd(self,ind):
		if ind == 0:  #left
			return (0,-1)
		elif ind ==1: #right
			return (0,1)
		elif ind ==2: #down
			return (1,0)
		elif ind ==3: #up
			return (-1,0)

	def count(self):
		c=[0 for y in range(self.n+1)]
		for y in range(self.d):
			for x in range(self.d):
				c[self.space[y][x]]+=1
		return c

	def isConnected(self,y,x,count,hops,last):#arrrgh think about me later
		if (count == (self.n-1)):
			#print "1"
			return True
		else:
			neighb=self.checkNeighbourhood(y,x)
			if (last+1 in neighb):
				ind=neighb.index(last+1)
				return self.isConnected(y+self.getInd(ind)[0],x+self.getInd(ind)[1],count+1,hops,last+1)
			else:
				if hops == -1:
					return False
				elif hops >= 0:
					results=[]
					neighb=self.checkNeighbourhood(y,x)
					for i in range(4):
						y1,x1=self.getInd(i)
						if neighb[i] > 0:
							results.append(self.isConnected(y+y1,x+x1,count,hops-1,last))

					if True in results:
						return True
						
					else:
						return False

	def connectedNets(self,hops):
		connected=0
		for y in range(self.d):
			for x in range(self.d):
			
				if self.space[y][x]==1:
					a=self.isConnected(y,x,0,hops,1)
					#print a
					if a==True:
						#print "y"
						connected=connected+1
		return connected




	def set(self,y,x,state):
		self.space[y][x]=state

	def checkNeighbourhood(self,y,x):
		#left node 

		#-1 == out of boundary
		if (x-1) > -1:
			left=self.space[y][x-1]
		else:
			left= -1

		if (x+1) < self.d:
			right=self.space[y][x+1]
		else:
			right= -1
		
		if (y+1) < self.d:
			down = self.space[y+1][x]
		else:
			down= -1
		
		if (y-1) > -1:
			up=self.space[y-1][x]
		else:
			up= -1
		return [left,right,down,up]

	def states(self,y,x,checkSpace):
		#Check neighbourhood:
		#Firstly check for a stochastic event:
		#Fault causing cell to death - state = 0
		
		#Request to divide :
		#Cell dies due to: 
			#scale down/ no app
			#internal corruption/fault
			#external corruption/fault
		r=random.random()
		if (checkSpace[y][x]!=0):

			if r<=self.deathProb:   #probability of node dieing
				self.space[y][x]=0
				#print 'die'
				return 0

			neighb=self.checkNeighbourhood(y,x)
			ch={}
			 #if a neighbour has the same function then differentiate
			if (checkSpace[y][x] in neighb): #calculate the qty of each function
				for f in self.functions:
					if f !=0:
						ch[f]=0
						for n in neighb:
							if n==f:
								ch[f]=ch[f]+1


				m = ch[min(ch.keys(), key=(lambda k: ch[k]))] #find the minimum 
				a=[]
				for key, value in ch.iteritems():
					if value == m:
						a.append(key)




					# print ch
				if self.choice==0:
					self.space[y][x]=random.choice(a) #differentiate to random
					#elif self.choice==1:
						#100%= pure diversity
						#0% = homogoneity
						#Add all disimilar neighbours to list 
						#divide |list| by quantity of functions gives diversity metric
						#divide to metric not in list

						
			if r<=self.divProb:		#probility of division request
				
				func=range(1,self.n+1)
				random.shuffle(func)
				for f in func:
					if (f not in neighb) and (self.space[y][x] != f):
						new=f
					else:
						new=random.choice(func) 


				for n in neighb:
					if n == 0:
						if neighb.index(n) == 0:  #left
							self.space[y][x-1]=new
						elif neighb.index(n) ==1: #right
							self.space[y][x+1]=new
						elif neighb.index(n) ==2: #down
							self.space[y+1][x]=new
						elif neighb.index(n) ==3: #up
							self.space[y-1][x]=new

						return

 	def setUpdateMode(self,m):
 		self.updateMode=m
