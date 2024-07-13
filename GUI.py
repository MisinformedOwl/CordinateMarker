# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:37:16 2024

@author: MisinformedOwl
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pickle
from glob import glob
import os

class GUI(tk.Tk):
    mode = "BoundingBoxes"
    boxCords = [(0,0),(0,0)]
    savedCords = []
    count = 0
    imageList = []
    imageSize = (0,0)
    
#------------------------------------------------------------------------------

    def loadImages(self):
        self.imageList = sorted(glob("images/*.jpg"), key=os.path.getmtime)
        i = Image.open(self.imageList[0])
        self.imageSize = i.size
        
#------------------------------------------------------------------------------
    
    def imageOnCanvas(self):
        self.canvas.delete("img")
        # Update the img attribute with the new PhotoImage object
        self.img = ImageTk.PhotoImage(file=self.imageList[self.count])
        self.canvas.create_image(10, 10, image=self.img, anchor='nw', tags="img")

#------------------------------------------------------------------------------
    
    def saveToFile(self):
        with open("cords.pkl", "wb") as file:
            pickle.dump(self.savedCords, file)

#------------------------------------------------------------------------------
    
    def saveCords(self):
        cords = [(x - 10, y - 10) for x, y in self.boxCords] # Had to add +10 becasue no matter what the canvas just refuses to anchor to NW.
        self.savedCords.append(list(cords))
        self.count+=1
        self.imageOnCanvas()
    
#------------------------------------------------------------------------------

    def drawBox(self):
        self.canvas.delete("box")
        box = self.canvas.create_rectangle(self.boxCords[0], self.boxCords[1], tag="box")
        
        if self.boxCords[0][0] > self.boxCords[1][0] or \
        self.boxCords[0][1] > self.boxCords[1][1]:
            
            self.canvas.itemconfig("box", outline="red")
        else:
            self.canvas.itemconfig("box", outline="black")
        
#------------------------------------------------------------------------------

    def boundingBoxClick(self, event):
        if event.num == 1:
            t = "left"
            self.boxCords[0] = (event.x, event.y)
        else:
            t = "right"
            self.boxCords[1] = (event.x, event.y)
            
        self.canvas.delete(f"{t}")
        self.canvas.create_oval((event.x-3, event.y-3), (event.x+3, event.y+3), tag =f"{t}")
        
        self.drawBox()
        
#------------------------------------------------------------------------------
        
    def __init__(self):
        self.loadImages()
        
        # Create a Tkinter window
        root = tk.Tk()
        root.title("Cordinate Capture")
            
        self.canvas = tk.Canvas(root, width=self.imageSize[0], height=self.imageSize[1], bg="white")
        self.imageOnCanvas()
        self.canvas.bind("<Button-1>", self.boundingBoxClick)
        self.canvas.bind("<Button-3>", self.boundingBoxClick)
        self.canvas.pack(anchor='nw', side='top', fill='both', expand=True)
        
        self.Button = tk.Button(root, text = "Save", command=self.saveCords)
        self.Button.pack()
        
        root.mainloop()
        self.saveToFile()
        


GUI()