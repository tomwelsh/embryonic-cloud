import ca
import random
import matplotlib.pyplot as plt
import sys
import Tkinter






death=float(sys.argv[1])
div=float(sys.argv[2])
steps=int(sys.argv[3])
functions=int(sys.argv[4])

c=ca.ca(10,functions,death,div)


#for i in range(5):
#	r=random.randint(0,9)
#	r2=random.randint(0,9)
#	c.set(r,r2,1)
c.set(4,4,1)
c.set(4,5,1)
c.set(4,6,1)
#c.set(5,5,2)
#c.set(5,6,3)
#c.set(5,6,3)

countData=[]
netData=[]
netData2=[]
temp=[]
avgNets2=0
avgNets=0
avgFuncs=[0 for x in range(functions+1)]
try:
	i=0
	for i in range(int(steps)):

		#i+=1
		print "Step: %d\n" % i
		c.step()
		space=c.space
		#print space[9][8]
		#print space
		connect=c.connectedNets(0)
		connect2=c.connectedNets(1)
		print "Connected nets: " + str(connect)
		print "Connected2 nets: " + str(connect2)
		#c.printSpace()
		co=c.count()
		countData.append(co)
		print co
		avgFuncs=[avgFuncs[j] + co[j] for j in range(0,len(co))]
		netData.append(connect)
		netData2.append(connect2)
		temp.append(float(netData[i])/countData[i][1])
		avgNets=avgNets+((float(netData[i]))/countData[i][1])
		avgNets2=avgNets2+((float(netData2[i]))/countData[i][1])
		#print float(netData[i])/countData[i][1]
		#temp.append(netData[i-1]/countData[i-1][1])
		c.printSpace()
		#raw_input("")
	print "\nAverages:"
	print [x/i for x in avgFuncs]
	print " Average connected Nets: " + str(avgNets/i)
	print " Average connected Nets 2 hops: " + str(avgNets2/i)
		#raw_input("")
	#plt.plot(countData,linestyle='--')
	#plt.plot(netData)]
	#plt.plot(temp)
	plt.plot([x[0] for x in countData],linestyle='-')
	plt.plot([x[1] for x in countData],linestyle=':')
	plt.xlabel('Time(t)', fontsize=12)
	plt.ylabel('Cells', fontsize=12)
	plt.show()

except KeyboardInterrupt:
	#plt.plot(countData)
	#plt.show()
	pass
