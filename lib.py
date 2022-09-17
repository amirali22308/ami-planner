import pygame as pg
import tkinter as tk

class text_item:
    def __init__(self,text : str,pos : tuple,font : pg.font.Font):
        self.text = text
        self.original = font.render(text,True,(25,25,25))
        self.pos = pos
        self.scale = 1
        self.font = font
        self.render = self.original
    def new_scale(self,scale : int):
        rect = self.original.get_rect()
        self.render = pg.transform.scale(self.original,(scale * rect.width,scale * rect.height))
        self.scale = scale
    def change_text(self,new_text : str):
        self.original = self.font.render(new_text,True,(25,25,25))
        rect = self.original.get_rect()
        self.render = pg.transform.scale(self.original,(self.scale * rect.width,self.scale * rect.height))
class image_item:
    def __init__(self,image_path : str,pos : tuple):
        self.path = image_path
        self.original = pg.image.load(image_path)
        self.pos = pos
        self.scale = 1
        self.render = self.original
    def new_scale(self,scale : int):
        rect = self.original.get_rect()
        self.render = pg.transform.scale(self.original,(scale * rect.width,scale * rect.height))
        self.scale = scale
class line_class:
    def __init__(self,start : tuple,end :tuple,width : int):
        self.start = start
        self.end = end
        self.width = width
def get_input(title : str):
    root= tk.Tk()
    root.title(title)
    root.wm_attributes('-toolwindow', 'True')

    canvas1 = tk.Canvas(root, width = 400, height = 100)
    canvas1.pack()

    entry1 = tk.Entry(root) 
    canvas1.create_window(200, int(75/2), window=entry1,height=25,width=300)
    
    result = []

    def getSquareRoot ():
        result.append(entry1.get())
        root.destroy()
    
    button1 = tk.Button(root,text='submit change', command=getSquareRoot)
    canvas1.create_window(200, 75, window=button1)
    root.mainloop()

    return result[0]