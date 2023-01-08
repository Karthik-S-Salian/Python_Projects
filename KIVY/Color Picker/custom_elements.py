from io import BytesIO
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout


class DynamicImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,1)
        self.allow_stretch=True
        self.keep_ratio=False

    def update_colormap(self,image):
        data=BytesIO()
        image.save(data,format="png")
        data.seek(0)
        im=CoreImage(BytesIO(data.read()),ext="png")
        self.texture=im.texture


class ColorView(Button):
    color=ListProperty([0,0,0])
    def __init__(self,color,callback, **kwargs):
        super().__init__(**kwargs)
        self.color=color
        self.on_selection=callback
        if len(color)==4:
            self.background_color=(color[0]/255,color[1]/255,color[2]/255,color[3])
        else:
            self.background_color=(color[0]/255,color[1]/255,color[2]/255)


class Color_data_container(RelativeLayout):
    bg_color=ListProperty([0,0,0])
    def __init__(self,color_data ,color_index,callback,**kwargs):
        super().__init__(**kwargs)
        self.bg_color=(50/255,70/255,100/255) if color_index else (70/255,80/255,120/255)
        self.add_widget(ColorView(color_data[1],callback,pos_hint={"center_y":.5,"x":.02}))
        self.add_widget(Label(text=color_data[0],pos_hint={"center_y":.5,"center_x":.6},size_hint=(.5,1)))

