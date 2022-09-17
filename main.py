import pygame as pg
from tkinter import filedialog
import tkinter as tk
import os

class text_item:
    def __init__(self,text : str,pos : tuple,font : pg.font.Font):
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

def main():
    pg.init()
    screensize = (600,700)
    win = pg.display.set_mode(screensize)
    pg.display.set_caption("ami planer")


    hot_bar_h = 0.1
    hot_bar_rect = pg.Rect(0,0,screensize[0],int(screensize[1] * hot_bar_h))
    hot_bar_color = (150,150,150)


    is_holding_right = False
    camera_position = [0,0]
    last_mouse_pos = [0,0]
    last_mouse_pos[0], last_mouse_pos[1] = pg.mouse.get_pos ()
    def move_cam():
        new_mouse_pos = [0,0]
        new_mouse_pos[0],new_mouse_pos[1] = pg.mouse.get_pos()
        if is_holding_right:
            camera_position[0] += new_mouse_pos[0] - last_mouse_pos[0]
            camera_position[1] += new_mouse_pos[1] - last_mouse_pos[1]
        last_mouse_pos[0], last_mouse_pos[1] = new_mouse_pos[0], new_mouse_pos[1]

    full_path = os.path.realpath(__file__)
    path = os.path.dirname(full_path) + chr(92)
    font = pg.font.Font(path + "font.ttf",15)
    pg.display.set_icon(pg.image.load(path + "logo.png"))
    all_text = []
    all_images = []
    all_lines = []


    selected_item_color = (15,15,15)
    target_func = [None]
    start_of_line = [None]
    make_line_i = pg.image.load(path + "add_l.png")
    def make_line_p1(pos):
        start_of_line[0] = pos
        target_func[0] = make_line_p2
    def make_line_p2(pos):
        all_lines.append(line_class(start_of_line[0],pos,3))
        target_func[0] = make_line_p1
    delete_line_i = pg.image.load(path + "delete_l.png")
    def delete_line(pos):
        target = None
        for line in all_lines:
            dis_all = (line.start[0] - line.end[0])**2 + (line.start[1] - line.end[1])**2
            dis_all **= 0.5
            dis_1 = (line.end[0] - pos[0])**2 + (line.end[1] - pos[1])**2
            dis_1 **= 0.5
            dis_2 = (line.end[0] - pos[0])**2 + (line.end[1] - pos[1])**2
            dis_2 **= 0.5
            if (dis_1 + dis_2) <= dis_all:
                target = line
                break
        if target != None:
            all_lines.remove(target)
    make_image_i = pg.image.load(path + "add_i.png")
    def create_image(pos):
        tk.Tk().withdraw()
        filename = filedialog.askopenfilename(
        initialdir = "/",title = "Select an Image"
        ,filetypes = (("Png files", "*.png*"),))
        all_images.append(image_item(filename,pos))
    make_text_i = pg.image.load(path + "add_t.png")
    def create_text(pos):
        all_text.append(text_item(get_input("insert text"),pos,font))
    target_item_to_move = [None]
    move_item_i = pg.image.load(path + "edit_pos.png")
    def move_item_p1(pos):
        target_item_to_move[0] = None
        for item in all_text:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    target_item_to_move[0] = item
                    break
        for item in all_images:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    target_item_to_move[0] = item
                    break
        if (target_item_to_move[0] != None):
            target_func[0] = move_item_p2
    def move_item_p2(pos):
        target_item_to_move[0].pos = pos
        target_func[0] = move_item_p1
    change_scale__i = pg.image.load(path + "edit_scale.png")
    def change_scale(pos):
        for item in all_text:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    item.new_scale(int(get_input()))
                    return
        for item in all_images:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    item.new_scale(int(get_input()))
                    return
    change_text_i = pg.image.load(path + "edit_t.png")
    def change_text(pos):
        for item in all_text:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    item.change_text(get_input("insert new text"))
                    break 
    delete_item_i = pg.image.load(path + "delete_item.png")
    def delete_item(pos):
        remove_t = None
        remove_i = None
        for item in all_text:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    remove_t = item
                    break
        for item in all_images:
            rect = item.render.get_rect()
            if item.pos[0] <= pos[0] and pos[0] <= (item.pos[0]+rect.width):
                if item.pos[1] <= pos[1] and pos[1] <= (item.pos[1]+rect.height):
                    remove_i = item
                    break
        if remove_i != None:
            all_images.remove(remove_i)
        if remove_t != None:
            all_text.remove(remove_t)


    target_func[0] = None

    loop = True
    while loop:
        #logic
        move_cam()
        #draw
        win.fill((255,255,255))

        for line in all_lines:
            pg.draw.line(win,(0,0,0),line.start,line.end,3)
        for item in all_text:
            render_pos = (item.pos[0] + camera_position[0],
            item.pos[1] + camera_position[1])
            win.blit(item.render,render_pos)
        for item in all_images:
            render_pos = (item.pos[0] + camera_position[0],
            item.pos[1] + camera_position[1])
            win.blit(item.render,render_pos)

        pg.draw.rect(win,hot_bar_color,hot_bar_rect)

        item_h = int(hot_bar_h/10 * screensize[1])
        target_func = target_func[0]
        if target_func == make_line_p1:
            pg.draw.rect(win,selected_item_color,pg.Rect(2,item_h-3,make_line_r.width+6,make_line_r.height+6))
        win.blit(make_line_i,(5,item_h))
        make_line_r = make_line_i.get_rect()

        if target_func == delete_line:
            pg.draw.rect(win,selected_item_color,pg.Rect(72,item_h-3,delete_line_r.width+6,delete_line_r.height+6))
        win.blit(delete_line_i,(75,item_h))
        delete_line_r = delete_line_i.get_rect()
        
        if target_func == create_image:
            pg.draw.rect(win,selected_item_color,pg.Rect(142,item_h-3,make_image_r.width+6,make_image_r.height+6))
        win.blit(make_image_i,(145,item_h))
        make_image_r = make_image_i.get_rect()

        if target_func == create_text:
            pg.draw.rect(win,selected_item_color,pg.Rect(212,item_h-3,make_text_r.width+6,make_text_r.height+6))
        win.blit(make_text_i,(215,item_h))
        make_text_r = make_text_i.get_rect()

        if target_func == move_item_p1:
            pg.draw.rect(win,selected_item_color,pg.Rect(282,item_h-3,move_item_r.width+6,move_item_r.height+6))
        win.blit(move_item_i,(285,item_h))
        move_item_r = move_item_i.get_rect()
        
        if target_func == change_scale:
            pg.draw.rect(win,selected_item_color,pg.Rect(352,item_h-3,change_scale__r.width+6,change_scale__r.height+6))
        win.blit(change_scale__i,(355,item_h))
        change_scale__r = change_scale__i.get_rect()
        
        if target_func == change_text:
            pg.draw.rect(win,selected_item_color,pg.Rect(422,item_h-3,change_text_r.width+6,change_text_r.height+6))
        win.blit(change_text_i,(425,item_h))
        change_text_r = change_text_i.get_rect()
        
        if target_func == delete_item:
            pg.draw.rect(win,selected_item_color,pg.Rect(492,item_h-3,delete_item_r.width+6,delete_item_r.height+6))
        win.blit(delete_item_i,(495,item_h))
        delete_item_r = delete_item_i.get_rect()
        target_func = [target_func]

        pg.display.update()
        #input
        for e in pg.event.get():
            if e.type == pg.QUIT:
                loop = False
                break
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 3:
                    is_holding_right = True
                if e.button == 1:
                    if last_mouse_pos[1] <= hot_bar_h * screensize[1]:
                        y = 1
                        if 5 <= last_mouse_pos[0] and last_mouse_pos[0] <= 5+make_line_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+make_line_r.height:
                                target_func = make_line_p1
                        elif 75 <= last_mouse_pos[0] and last_mouse_pos[0] <= 75+delete_line_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+delete_line_r.height:
                                target_func = delete_line
                        elif 145 <= last_mouse_pos[0] and last_mouse_pos[0] <= 145+make_image_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+make_image_r.height:
                                target_func = create_image
                        elif 215 <= last_mouse_pos[0] and last_mouse_pos[0] <= 215+make_text_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+make_text_r.height:
                                target_func = create_text
                        elif 285 <= last_mouse_pos[0] and last_mouse_pos[0] <= 285+move_item_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+move_item_r.height:
                                target_func = move_item_p1
                        elif 355 <= last_mouse_pos[0] and last_mouse_pos[0] <= 355+change_scale__r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+change_scale__r.height:
                                target_func = change_scale
                        elif 425 <= last_mouse_pos[0] and last_mouse_pos[0] <= 425+change_text_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+change_text_r.height:
                                target_func = change_text
                        elif 495 <= last_mouse_pos[0] and last_mouse_pos[0] <= 495+delete_item_r.width:
                            if item_h <= last_mouse_pos[y] and last_mouse_pos[y] <= item_h+delete_item_r.height:
                                target_func = delete_item
                        else:
                            target_func = None
                        target_func = [target_func]
                    elif target_func[0] != None:
                        target_func[0]([last_mouse_pos[0] - camera_position[0],last_mouse_pos[1] - camera_position[1]])
            if e.type == pg.MOUSEBUTTONUP:
                if e.button == 3:
                    is_holding_right = False


if __name__ == "__main__":
    main()