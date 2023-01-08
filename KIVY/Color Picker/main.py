from kivy.config import Config

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder

from re import findall
from json import load
from collections import deque

from utils import ColorMap
from custom_elements import DynamicImage,ColorView,Color_data_container

Window.clearcolor = (77/255, 80/255, 105/255, 1)
Builder.load_file("custom_elements.kv")


class MainAppLayout(BoxLayout):
    color=ListProperty([0,0,0,0])
    pointer_pos=ListProperty([0,0])
    recents=ListProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_utils=ColorMap()
        self.color_data=dict()
        self.hsv=[0,.5,0.5]
        self.rgb=[1,1,1,1]
        self.hex='sbasasbk'
        self.pointer_pos=[0,0]
        self.alpha=1
        self.recents=deque(maxlen=10)
        self.is_running=False


    def on_parent(self,j,k):
        if not self.is_running:
            self.h_scale=self.ids.h_scale_slider
            self.alpha_scale=self.ids.alpha_scale_slider
            self.color_list_container=self.ids.color_list_container
            self.color_map:DynamicImage=self.ids.color_map
            self.recent_color_container=self.ids.recent_color_container
            self.on_h_slider_update(self.hsv[0])
            self.load_recent_colors()
            standard_color_list=load(open(r"resources\\data\\color_data.json"))['standard_colors']
            for i,color_data in enumerate(standard_color_list):
                self.color_list_container.add_widget(Color_data_container(color_data,i%2,self.on_user_color_selection))
            for color in self.recents:
                self.recent_color_container.add_widget(ColorView(color,self.on_user_color_selection))
            self.is_running=True
        else:
            with open(r"resources\\data\\recent_colors.txt",'w') as f:
                f.write(str(list(self.recents)))

    
    def load_recent_colors(self):
        with open(r"resources\\data\\recent_colors.txt") as f:
            q=deque(findall(r'\(.*?\)',f.read()),maxlen=10)
            for ele in q:
                x,y,z,a=findall(r"[0-9.]+",ele)
                x,y,z,a=int(x),int(y),int(z),float(a)
                self.recents.append((x,y,z,a))
        
    
    def update_color_map(self,h):
        image=self.color_utils.colormap_image_generator(h)
        self.color_map.update_colormap(image)

    def on_user_color_selection(self,color):
        self.on_rgb_color_update(color)
        self.h_scale.value=self.hsv[0]
        self.alpha_scale.value=round(self.alpha*100)


    def on_h_slider_update(self,h):
        self.hsv[0]=int(h)
        self.update_color_map(h)
        self.on_hsv_color_update()


    def on_touch_move(self, touch):
        self.on_mouse_input(touch)
        return super().on_touch_move(touch)

    def on_touch_down(self, touch):
        self.on_mouse_input(touch)
        return super().on_touch_down(touch)

    def on_mouse_input(self,touch):
        x,y=touch.pos[0]-self.color_map.pos[0],touch.pos[1]-self.color_map.pos[1]      
        if (self.color_map.collide_point(*touch.pos)):
            self.hsv=[self.hsv[0],round(x/self.color_map.width,2),round(y/self.color_map.height,2)]
            self.on_hsv_color_update(touch.pos)

    def on_hsv_color_update(self,pos=None):
        x,y,z=self.color_utils.hsv_to_rgb(*self.hsv)
        self.rgb=(int(x),int(y),int(z))
        self.hex=self.color_utils.rgb_to_hex(*self.rgb)
        self.color=x/255,y/255,z/255,self.alpha
        self.update_pointer_pos(pos)
        self.update_labels()

    def on_rgb_color_update(self,rgba):
        if len(rgba)==3:
            x,y,z=rgba
            self.alpha=1
        elif len(rgba)==4:
            self.alpha=rgba[3]
            x,y,z=rgba[:3]
        self.rgb=x,y,z=(int(x),int(y),int(z))
        self.hsv=list(self.color_utils.rgb_to_hsv(x,y,z))
        self.hex=self.color_utils.rgb_to_hex(x,y,z)
        self.color=x/255,y/255,z/255,self.alpha
        self.update_pointer_pos()
        self.update_labels()
    

    def update_pointer_pos(self,pos=None):
        if pos:
            self.pointer_pos=pos
        else:
            x,y=self.color_map.pos
            w,h=self.color_map.size
            self.pointer_pos=x+w*self.hsv[1],y+h*self.hsv[2]

    def on_alpha_slider_update(self,value):
        self.alpha=value/100
        self.color=self.color[0],self.color[1],self.color[2],self.alpha
        self.ids.rgba_label.text=f"{self.rgb[0]} , {self.rgb[1]} , {self.rgb[2]} , {round(self.alpha,2)}"


    def update_labels(self):
        self.ids.rgba_label.text=f"{self.rgb[0]} , {self.rgb[1]} , {self.rgb[2]} , {round(self.alpha,2)}"
        self.ids.hsv_label.text=f"{int(self.hsv[0])} , {self.hsv[1]} , {self.hsv[2]} "
        self.ids.hex_label.text=self.hex

    def on_text_input_validate(self,text,c_type):
        valid=False
        if c_type=="rgba":
            out=findall(r"[0-9]+",text)
            if len(out)==3:
                value=int(out[0])%256,int(out[1])%256,int(out[2])%256
                self.alpha=1
                self.on_user_color_selection(value)
                valid=True
            elif len(out)==4:
                a=int(out[3])
                value=int(out[0])%256,int(out[1])%256,int(out[2])%256,a if 0<=a<=1 else 1
                self.alpha=1
                self.on_user_color_selection(value)
                valid=True
        elif c_type=="hsv":
            out=findall(r"[0-9]+",text)
            if len(out)==3:
                b,c=int(out[1]),int(out[2])
                hsv=int(out[0])%360,b if 0<=b<=1 else 1,c if 0<=c<=1 else 1
                rgb=self.color_utils.hsv_to_rgb(hsv)
                self.alpha=1
                self.on_user_color_selection((*rgb,1))
                valid=True
        elif c_type=="hex":
            out = findall(r"^#[0-9]{6}",text)
            if out:
                rgb=self.color_utils.hex_to_rgb(out[0])
                self.alpha=1
                self.on_user_color_selection((*rgb,1))
                valid=True
        if not valid:
            self.update_labels()

    def update_recents(self):
        if not self.recents[-1] == (*self.rgb,self.alpha):
            self.recent_color_container.clear_widgets([self.recent_color_container.children[-1]])
            self.recent_color_container.add_widget(ColorView(self.rgb,self.on_user_color_selection))
            self.recents.append((*self.rgb,self.alpha))


if __name__=="__main__":
    class MainApp(App):
        pass

    MainApp().run()

