from kivy.app import App
from kivy.uix.image import Image,AsyncImage
from kivy.properties import ListProperty,ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import os
from urllib.error import URLError
from tkinter import filedialog



def load_color_data():
    with open(r"D://Users//Dell//Documents//PythonProjects//KIVY//Color Detector//color_names.csv","r") as f:
        d=dict()
        for line in f.readlines():
            color,r,g,b=line.split(",")
            r,g,b=int(r),int(g),int(b)
            d[r]=d.get(r,dict())
            d[r][g]=d[r].get(g,dict())
            d[r][g][b]=color
        return d

class LoadDialog(Popup):
    load_file = ObjectProperty(None)
    load_url = ObjectProperty(None)
    cancel = ObjectProperty(None)

class CustomImage(AsyncImage):
    floatpos=ListProperty([0,0])
    crr_color=ListProperty([0,0,0])
    def __init__(self, **kwargs):
        super(CustomImage, self).__init__(**kwargs)

    def collide_point(self, x, y):
        img_size_x,img_size_y=self.norm_image_size
        size_x,size_y=self._coreimage.size
        cx,cy=self.center
        pixel_x,pixel_y=(-cx+img_size_x/2 + x)/img_size_x*size_x,(img_size_y/2+cy-y)/img_size_y*size_y
        if 0<=pixel_x<=size_x:
            if 0<=pixel_y<=size_y:
                color = self._coreimage.read_pixel(pixel_x,pixel_y)
                return color

    def on_touch_down(self, touch):
        collide_color=self.collide_point(*touch.pos)
        
        if collide_color:
            self.floatpos=touch.pos
            self.crr_color=collide_color
        
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        collide_color=self.collide_point(*touch.pos)
        
        if collide_color:
            self.floatpos=touch.pos
            self.crr_color=collide_color

        return super().on_touch_move(touch)

    def on_crr_color(self,j,k):
        self.parent.update_color(self.crr_color)


class MainLayout(BoxLayout):

    crr_color =ListProperty([0,0,0])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.maintain_ratio=True
        self.image_obj=None
        self.color_data:dict=load_color_data()
        self.color_name=None

    def on_parent(self,j,k):
        self.image_obj:CustomImage=self.ids.cimage
        self.crr_color=self.image_obj.crr_color

    def update_color(self,color):
        self.color_name=self.color_data.get(int(color[0]*255),dict()).get(int(color[1]*255),dict()).get(int(color[2]*255),None)
        self.crr_color=color


    def change_image_ratio(self):
        self.image_obj.keep_ratio=not self.image_obj.keep_ratio
        return self.image_obj.keep_ratio

    def on_new_prompt(self):
        self._popup = LoadDialog(title="NEW",size_hint=(0.9, 0.9),load_file=self.load_local_file,load_url=self.load_from_url, cancel=self.dismiss_popup)
        self._popup.open()

    def load_local_file(self):
        file=filedialog.askopenfilename()
        if file:
            self.image_obj.source=file
        self.dismiss_popup()

    def load_from_url(self,url):
        self.image_obj.error_image=self.image_obj.source
        self.image_obj.source=url

    def dismiss_popup(self):
        self._popup.dismiss()


        



if __name__ == '__main__':
    class ColorDetectorApp(App):
        pass
    ColorDetectorApp().run()
