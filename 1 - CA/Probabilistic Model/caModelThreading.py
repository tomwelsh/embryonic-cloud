import sys
import threading
#PYTHON VERSION 3!!!!

#q=int(sys.argv[1])
#f=float(sys.argv[2])
#n=5
#print(f)
lock=threading.Lock()
results=0
def probTree(mov,prob):
	global results
	if mov==q-1: #if we have moved all the way through tree
		#print("found %f" % prob)
		#lock.acquire()
		results=results+prob
		#lock.release()
		#results=results+prob
		return prob
	else:    #if we have not moved all the way through tree
		j=0
		for i in range(n):
			j=j+(f**(i+1))
		notfail=1-j
		#print(notfail)
		#p(0 fail)
		if q<n: # if > 100% set to 100% 
			q2=n
		else:
			q2=q
		if mov ==0 :
			t=threading.Thread(target=probTree,args=((mov+1),((notfail*(n/q2)*prob)),))
			t.start()
			t.join()
		else:
			res=probTree((mov+1),((notfail*(n/q2)*prob)))
			#right (n) branch move
		###right branch
		for i in range(n):
			#aNodes=1-((i+1)/n)
			aNodes=((n+1)-(i+1))/q2
			failProb=f**(i+1)
			if mov!=-1:
				t=threading.Thread(target=probTree,args=((mov+1),(failProb*aNodes*prob)))
				t.start()
				t.join()
			else:
				probTree((mov+1),(failProb*aNodes*prob)) #left
tRes=[]
n=13
for q in range(7,8):
	print(q)
	res=[q]
	for f in [0.1,0.2,0.3,0.4]:	
		print(f)
		results=0
		probTree(0,1)
		res.append(results)
	tRes.append(res)

print("q,",end="")
for f in [0.1,0.2,0.3,0.4]:
	print(str(f)+",",end="")
for r in tRes:
	print()
	for r2 in r:
		print(str(r2)+",",end="")
print()