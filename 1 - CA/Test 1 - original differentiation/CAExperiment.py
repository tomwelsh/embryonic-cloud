#CA Experiment with GUI

import ca
import random
import matplotlib.pyplot as plt
import sys
import pygubu
from Tkinter import *
import tkMessageBox


class MainWindow():

		def __init__(self,main,nodesize):
			self.count=0
			self.started=False
			self.builder = builder = pygubu.Builder()
			builder.add_from_file('CAEXPGui.ui')
			self.mainwindow = builder.get_object('topLevel', main)
			builder.connect_callbacks(self)
			self.canvas1=self.builder.get_object('canvas1')
			self.running=False
			self.countData=[]
			self.countLbl=self.builder.get_object('countLbl')
			self.updateCount()

			#self.MainLabel=Label(main,text="CA Resilience GUI").grid(row=0
			#self.canvas = Canvas(main,)
			#self.canvas.grid(row=0, column=0,sticky=E)
			#self.nextBtn = Button(main, text="Step", command=self.onNextButton)
			#self.nextBtn.grid(row=1, column=0)
			#self.faultScale = Scale(main, from_=0, to=1,resolution=0.1,label="Fault Rate",orient=HORIZONTAL)
			#self.faultScale.grid(row=0,column=1)
			#self.divScale = Scale(main, from_=0, to=1,resolution=0.1,label="Div Rates",orient=HORIZONTAL)
			#self.divScale.grid(row=1,column=1)
		#	self.backBtn = Button(main, text="Change", command=self.onBackButton)
			####CA init stuff

		def updateCount(self):
			self.countLbl.configure(text="Step : " + str(self.count))


		def onNextButton(self):
			if self.started==False:
				tkMessageBox.showinfo('Error', 'Please create CA')
			else:
				self.c.step()
				space=self.c.space
				self.countData.append(self.c.count())
				#print space
				#c.printGrid()
				#print c.count()
				sq=10*20
				for x in range(0,sq,20):
					for y in range(0,sq,20):
						if (x % 20 == 0) and (y % 20==0):
							if space[x/20][y/20]==0:
								col="white"
							elif space[x/20][y/20]==1:
								col="green"
							elif space[x/20][y/20]==2:
								col="blue"
							elif space[x/20][y/20]==3:
								col="red"
							elif space[x/20][y/20]==4:
								col="yellow"
							elif space[x/20][y/20]==5:
								col="orange"
							else:
								col="green"

							self.canvas1.create_rectangle(x,y,x+20,y+20, fill=col)
				self.count+=1
				self.updateCount()
				#countData.append(c.count())


		def onStartButton(self):


			if self.started==True:
				result = tkMessageBox.askquestion("Restart?", "Are You Sure?", icon='warning')
   				if result == 'no':
						return 0
				else:
					self.count=0
					self.updateCount()
					self.countData=[]
					sq=10*20
					for x in range(0,sq,20):
						for y in range(0,sq,20):
							if (x % 20 == 0) and (y % 20==0):
								self.canvas1.create_rectangle(x,y,x+20,y+20, fill="white")

			self.death=self.builder.get_object('deathScale').get()
			self.div=self.builder.get_object('divScale').get()
			self.functions=self.builder.get_object('funcSpin').get()
			self.c=ca.ca(10,int(self.functions),self.death,self.div)
			for i in range(5):
				r=random.randint(0,9)
				r2=random.randint(0,9)
				self.c.set(r,r2,1)
			self.started=True

		def onGraphButton(self):
			plt.plot(self.countData)
			plt.show()




#death=float(sys.argv[1])
#div=float(sys.argv[2])
#functions=int(sys.argv[3])

root = Tk()
app= MainWindow(root,10)
root.mainloop()
