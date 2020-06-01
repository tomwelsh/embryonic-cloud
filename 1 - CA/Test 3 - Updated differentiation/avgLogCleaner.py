#new log cleaner


import sys
print 'Functions,Deathrate,Spawnrate,NeighbourhoodStart,NeighbourhoodLocation,Run,Connected0,Connected1,Q0,Q1,Q2,Q3,Q4,Q5,Q6'
fIn=open(sys.argv[1],"r")
#fOut=open(sys.argv[1]+'cleaned',"w")
for line in fIn.readlines():
	s=line.index('[')
	e=line.index(']')
	qtys=line[s+1:e].split(',')
	while len(qtys)!=7:
		qtys.append('NULL')
	#print qtys
	new=line[:s]+line[e+2:]
	#print new#
	l=new.split(",")
	s="%d,%f,%f,%d,%d,%d,%f,%f" % (int(l[0].lstrip('F')),float(l[1].lstrip("D")),float(l[2].lstrip("S")),int(l[3].lstrip("N")),int(l[4].lstrip("L")),int(l[5].lstrip("R")),float(l[6]),float(l[7]))
	for q in qtys:
		s+=(','+str(q))
	print s