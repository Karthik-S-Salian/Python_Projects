from io import BytesIO

from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from numpy import zeros,uint8
from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.uix.relativelayout import RelativeLayout
from PIL import Image as PILImage



class ColorMap:

    def hsv_to_rgb(self,h, s, v):
        if s == 0.0: v *= 255; return (v, v, v)
        i = int(h * 6.)
        f = (h * 6.) - i
        p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
        v *= 255
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    def rgb_to_hsv(self,r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df / mx) * 100
        v = mx * 100
        return round(h), round(s), round(v)


    def colormap_image_generator(self,h):
        arr = zeros((255, 255, 3), dtype=uint8)
        for i in range(arr.shape[0]):
            v = 255 - i
            for j in range(arr.shape[1]):
                arr[i][j] = self.hsv_to_rgb(h / 360, j / 255, v / 255)

        return PILImage.fromarray(arr)

    
    def rgb_to_hex(self,r,g,b):
        return "#"+hex(r)+hex(g)+hex(b)

    def h_scale_generator(self):
        arr=zeros((30,360,3),dtype=uint8)
        for i in range(arr.shape[1]):
            for j in range(arr.shape[0]):
                arr[j][i]=self.hsv_to_rgb(i/360,1,1)
        
        return PILImage.fromarray(arr)


        
class ColorLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(ColorLayout, self).__init__(**kwargs)
        self.colormap = ColorMap()

        self.image_object = Image()
        self.add_widget(self.image_object)


    def update_colormap(self,h):
        data=BytesIO()
        img=self.colormap.colormap_image_generator(h)
        img.save(data,format="png")
        data.seek(0)
        im=CoreImage(BytesIO(data.read()),ext="png")
        self.image_object.texture=im.texture
        with self.canvas:
            Color(self.colormap.hsv_to_rgb(h,1,1))
            self.color_view = Rectangle()


class MainAppLayout(BoxLayout):

    def __init__(self,**kwargs):
        super(MainAppLayout, self).__init__(**kwargs)








if __name__=="__main__":
    class MainApp(App):
        pass

    MainApp().run()