import sys
import multiprocessing
import time
#PYTHON VERSION 3!!!!

#q=int(sys.argv[1])
#f=float(sys.argv[2])
#n=5
#print(f)

results=0
def probTree(mov,prob):
	global results
	if mov==q-1: #if we have moved all the way through tree
		results=results+prob
		return prob
	else:    #if we have not moved all the way through tree
		j=0
		for i in range(n):
			j=j+(f**(i+1))
		notfail=1-j
		#p(0 fail)
		if q<n: # if > 100% set to 100% 
			q2=n
		else:
			q2=q
		
		probTree((mov+1),((notfail*(n/q2)*prob)))
		###right branch
		for i in range(n):			
			aNodes=((n+1)-(i+1))/q2
			failProb=f**(i+1)
			probTree((mov+1),(failProb*aNodes*prob)) #left
fi=open('output%f' % time.time(),'w')
tRes=[]


n=13
fi.write(str(n)+'\n')
for q in range(2,16):
	print(q)
	res=[q]
	for f in [0.1,0.2,0.3,0.4]:	
		print(f)
		results=0
		probTree(0,1)
		res.append(results)
	tRes.append(res)

fi.write("q,")
print("q,",end="")
for f in [0.1,0.2,0.3,0.4]:
	print(str(f)+",",end="")
	fi.write(str(f)+",")
for r in tRes:
	fi.write("\n")
	print()
	for r2 in r:
		print(str(r2)+",",end="")
		fi.write(str(r2)+",")
print()