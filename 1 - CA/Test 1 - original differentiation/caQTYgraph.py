#CA graph log output

import sys
import matplotlib.pyplot as plt
f=open(sys.argv[1])

data=[]
ind=0
out=0
ind=0
linesIn=f.readlines()
for line in linesIn:
	t=line.find('2016')
	#print t
	if t > -1:
		data.append(ind)
	ind+=1

i=0

#print linesIn
for t in range(len(data)/2):
	print linesIn[i:i+1]
	i+=1
