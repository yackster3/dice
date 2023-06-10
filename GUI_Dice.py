from tkinter import *
from PIL import ImageTk, Image

WindowBackground = "black"

window = Tk() #instance of a window

window.geometry("840x840") #Window Dimensions
window.title("\"The die has been cast\"") #Change window name

icon = PhotoImage(file = 'Y3.png')
window.iconphoto(True,icon)




window.config(background = WindowBackground)

window.mainloop()#display window on screen
