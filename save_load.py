from lib import *
from os.path import exists
import pickle
#filename = filedialog.askopenfilename(
#        initialdir = "/",title = "Select an Image"
#        ,filetypes = (("Png files", "*.png*"),))

class saveable_text:
    def __init__(self,text : text_item):
        self.text = text.text
        self.pos = text.pos
        self.scale = text.scale
    @staticmethod
    def loader(text,font):
        result = text_item(text.text,text.pos,font)
        result.new_scale(text.scale)
        return result
class saveable_image:
    def __init__(self,image : image_item):
        self.path = image.path
        self.pos = image.pos
        self.scale = image.scale
    @staticmethod
    def loader(image):
        result = image_item(image.path,image.pos)
        result.new_scale(image.scale)
        return result


def save(all_text : list,all_images : list,all_lines : list,save_path : str):
    
    all_ts  = []
    for text in all_text:
        all_ts.append(saveable_text(text))
    all_is  = []
    for image in all_images:
        all_is.append(saveable_image(image))
    
    file = open(save_path + "/plan.ap",'wb')
    save_file = [all_ts,all_is,all_lines]
    pickle.dump(save_file,file)
    file.close()
    return True

def load(save_path : str,font):
    if not exists(save_path):
        return None
    file = open(save_path,'rb')
    save_file = pickle.load(file)
    file.close()

    all_text = []
    for text in save_file[0]:
        all_text.append(saveable_text.loader(text,font))
    all_images = []
    for image in save_file[1]:
        all_images.append(saveable_image.loader(image))
    return [all_text,all_images,save_file[2]]