from kivy.config import Config

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line,Rectangle
from kivy.properties import  Clock
from kivy.uix.widget import Widget
from math import sin,pi,cos
import numpy as np

class MainWidget(Widget):
    V_NB_LINES = 34
    V_LINES_SPACING = .25
    vertical_lines = []

    H_NB_LINES = 10
    H_LINES_SPACING = .1 
    horizontal_lines = []

    SPEED = 4
    current_offset_y = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_and_horizontal_lines()
        self.horizon_x=1
        self.horizon_y=1
        self.perspective_point_x = 1
        self.perspective_point_y = 1
        self.spacing_y=1
        self.deviation=pi/8
        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

    def on_parent(self, widget, parent):
        self.horizon_x = self.width/2
        self.horizon_y = self.height /2
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height *0.75

    def init_vertical_and_horizontal_lines(self):
        with self.canvas:
            Color(201/255, 32/255, 158/255)
            for _ in range(self.V_NB_LINES):
                self.vertical_lines.append(Line(width=1.2))
            for _ in range(self.H_NB_LINES):
                self.horizontal_lines.append(Line(width=1.2))
            self.vertical_line_points=np.zeros((self.V_NB_LINES,4))
            self.horizontal_line_points=np.zeros((self.H_NB_LINES,4))

    def init_line_parameters(self):
        # vertical 
        self.central_line_x = int(self.width / 2)
        self.vertical_spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES/2)+0.5
        for i in range(0, self.V_NB_LINES):
            line_x = self.central_line_x + (i+offset)*self.vertical_spacing
            self.vertical_line_points[i]=[line_x, 0, line_x, self.height*.99]

        #horizontal
        self.spacing_y = self.H_LINES_SPACING * self.height
        xmin = self.central_line_x-offset*self.vertical_spacing
        xmax = self.central_line_x+offset*self.vertical_spacing
        for i in range(0, self.H_NB_LINES):
            line_y = i*self.spacing_y
            self.horizontal_line_points[i]=[xmin, line_y, xmax, line_y]

    def on_size(self, *args):
        self.deviation=(pi/8)*(self.width/1000)
        with self.canvas.before:
            rect=Rectangle()
            rect.pos=self.pos
            rect.size=self.size
            rect.source='bg.png'
        self.horizon_x = self.width/2
        self.horizon_y = self.height /2
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height *0.75
        self.init_line_parameters()

    def update_vertical_lines(self,time_factor):
        for i in range(0, self.V_NB_LINES):
            x1,y1,x2,y2=self.vertical_line_points[i]
            x1,y1=self.transform(x1+self.current_offset_x,y1)
            x2,y2=self.transform(x2+self.current_offset_x,y2)
            self.vertical_lines[i].points = [x1,y1,x2,y2]

        self.current_offset_x += self.current_speed_x * time_factor
        if abs(self.current_offset_x) >= self.vertical_spacing:
            self.current_offset_x = 0

    def update_horizontal_lines(self,time_factor):
        for i in range(self.H_NB_LINES):
            x1,y1,x2,y2=self.horizontal_line_points[i]
            x1,y1=self.transform(x1,y1-self.current_offset_y)
            x2,y2=self.transform(x2,y2-self.current_offset_y)

            self.horizontal_lines[i].points = [x1,y1,x2,y2]
        
        self.current_offset_y += self.SPEED * time_factor
        if self.current_offset_y >= self.spacing_y:
            self.current_offset_y =0

    def transform(self, x, y):
        #return self.transform_2D(x, y)
        #return self.transform_perspective(x, y)
        return self.transform_horizon(x, y)

    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y-lin_y
        factor_y = diff_y/self.perspective_point_y
        factor_y = pow(factor_y, 4)

        tr_x = self.perspective_point_x + diff_x*factor_y
        tr_y = self.perspective_point_y - factor_y*self.perspective_point_y

        return int(tr_x), int(tr_y)

    def transform_horizon(self,x,y):
        self.horizon_y=self.height/2
        lin_y = y * self.horizon_y / self.height
        if lin_y > self.horizon_y:
            lin_y = self.horizon_y
        factor_y = (self.horizon_y-lin_y)/self.horizon_y
        factor_y = pow(factor_y, 4)

        diff_x = pow((self.horizon_x-x)/self.horizon_x,1)
        tr_x=x+y*diff_x*cos(self.deviation)
        tr_y = self.horizon_y - factor_y*self.horizon_y
        return int(tr_x),int(tr_y)

        

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        if touch.x < self.width/2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X

    def on_touch_up(self, touch):
        self.current_speed_x = 0

    def update(self, dt):
        time_factor = dt*60
        self.update_vertical_lines(time_factor)
        self.update_horizontal_lines(time_factor)
        

class SwedenApp(App):
    def build(x):
        return MainWidget()


SwedenApp().run()