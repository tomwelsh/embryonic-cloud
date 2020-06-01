#Script to run bulk tests for the CA for dataset generation

#We want to measure:
	# quantity of fully connected nets, consecutive
	# quantity of fully connected nets from
	# quantity of each function(>= 0)
	# other resilience things? --save space?


#We want to vary:
	# number of functions
	# death rate

	# initial starting conditions
			# qty
			# number of functions
			# location

#Will keep static:
	#step rate

import ca
import random
#import matplotlib.pyplot as plt
import time

#basic variables
deathRange=[i/10.0 for i in range(5)]
#spawRange=[i/10.0 for i in range(5,10)]
spawRange=[1]
functions=range(1,7)
steps=500
runs=10
#starting conditions
#
startQty=(1,5,9) #neighbourhoods of 1,5 and 9
startPos=[(4,4),(1,1),(1,8),(8,1),(8,8)] #center, top left, top right, bottom left, bottom right,

pos=[]


for p in startPos:
	temp=[]
	for q in startQty:
		st=[]
		st.append(p)
		if (q==5) or (q==9):
			st.append((p[0]+1,p[1]))
			st.append((p[0]-1,p[1]))
			st.append((p[0],p[1]+1))
			st.append((p[0],p[1]-1))
		if (q==9):
			st.append((p[0]-1,p[1]-1))
			st.append((p[0]+1,p[1]+1))
			st.append((p[0]-1,p[1]+1))
			st.append((p[0]+1,p[1]-1))
		temp.append(st)
	pos.append(temp)

mainLog=open('avgsLog'+str(time.time()),'w')
mapLog=open('mapLog'+str(time.time()),'w')
for curDeath in deathRange:
	for curSpaw in spawRange:
		for func in functions:
			for p in pos:
				for n in p:
					#n averages

					for r in range(runs):

						c=ca.ca(10,func,curDeath,curSpaw)
						if len(n)==1:
							c.set(n[0][0],n[0][1],1)
							#print 1
						elif len(n)>1:
							count=1
							for i in range(len(n)):
								if count==0: 
									count=count+1
								c.set(n[i][0],n[i][1],count)
								count=count+1
								count=count % func
						#run averages
						avgNet0=0
						avgNet1=0
						
						avgFuncs=[]
						avgFuncs=[0 for x in range(func+1)]

						fName="F%d,D%f,S%f,N%d,L%d,R%d" % (func,curDeath,curSpaw,len(n),pos.index(p),r)
						#fOut=open(fName+'.log','w')
						mapLog.write(time.strftime("%Y-%m-%d %H:%M")+','+fName+'\n')
						print fName
						for s in range(steps):
							#print "Step: %d\n" % s
							try:
								c.step()
								co=c.count()
								#countData.append(co)
								con0=c.connectedNets(0)
								con1=c.connectedNets(1)
								#space=c.space
								mapLog.write(str(co)+','+str(con0)+','+str(con1)+','+str([str(x) for x in c.space])+'\n')
								avgFuncs=[avgFuncs[j] + co[j] for j in range(0,len(co))]
								avgNet0=avgNet0+((float(con0))/co[1])
								avgNet1=avgNet1+((float(con1))/co[1])

							except ZeroDivisionError:
								mapLog.write('DEATH\n')
								break
						#fOut.close()
						mainLog.write(fName+','+str([x/steps for x in avgFuncs])+','+str(avgNet0/steps)+','+str(avgNet1/steps)+'\n')

mainLog.close()
mapLog.close()
				#	print ("%f,%f,%d") % (curDeath,curSpaw,func)
			#exp=ca.ca(10,func,curDeath,curSpaw)






		#for j in functions:
		#	for k in range(j):
		#		print p2[k] 
		#		print k+1



