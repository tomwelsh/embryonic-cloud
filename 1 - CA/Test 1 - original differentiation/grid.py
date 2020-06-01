import Tkinter



def printGrid(matrix):
	root = Tkinter.Tk()
	canvas = Tkinter.Canvas(root)
	canvas.pack()




	for x in range(0,100):
		for y in range(0,100):
			if (x % 20 == 0) and (y % 20==0):
				canvas.create_rectangle(x,y,x+20,y+20, fill="yellow")



	root.mainloop()

printGrid(None)