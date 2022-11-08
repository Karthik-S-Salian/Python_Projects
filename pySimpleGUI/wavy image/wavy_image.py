# ONLY PNG IMAGE WORKS IN PYSIMPLEGUI
import PySimpleGUI as sg
from PIL import Image, ImageOps
from io import BytesIO
from math import sin,pi

class WaveDeformer:
    def __init__(self,phase,size):
        self.phase=phase
        self.amp=size/20

    def transform(self, x, y):
        y = y + self.amp*sin(x/40 +self.phase)
        return x, y

    def transform_rectangle(self, x0, y0, x1, y1):
        return (*self.transform(x0, y0),
                *self.transform(x0, y1),
                *self.transform(x1, y1),
                *self.transform(x1, y0),
                )

    def getmesh(self, img):
        self.w, self.h = img.size
        gridspace = 20

        target_grid = []
        for x in range(0, self.w, gridspace):
            for y in range(0, self.h, gridspace):
                target_grid.append((x, y, x + gridspace, y + gridspace))

        source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

        return [t for t in zip(target_grid, source_grid)]
    

def update_image(original,phase,size):
    image=ImageOps.deform(original,WaveDeformer(phase,size))
    bio = BytesIO()
    image.save(bio, format = 'PNG')
    window['-IMAGE-'].update(data = bio.getvalue())

def load_image():
    image_path :str=sg.popup_get_file('Open',no_window = True)

    if not image_path.endswith('.png'):
        Image.open(image_path).save('current_img.png')
        image_path='current_img.png'

    return image_path,Image.open(image_path)
    #original=original.resize((int(original.size[0]*.5),int(original.size[1]*.5)))


if __name__=="__main__":
    image_path,original=load_image()

    layout = [[sg.Image(image_path, key = '-IMAGE-')]]
    window = sg.Window('WAVY Image', layout)

    phase=pi/12
    while True:
        event, values = window.read(timeout =100)
        if event == sg.WIN_CLOSED:
            break

        update_image(original,phase,original.size[1])
        phase+=pi/12
		
    window.close()