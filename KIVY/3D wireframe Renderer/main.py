from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.config import Config
from vertex_generator import cuboid
from transformer import rotateX, rotateY
from kivy.properties import Clock

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


class RedstoneDisplay(RelativeLayout):
    SPACING = dp(20)
    LINE_COLOR = (242 / 255, 237 / 255, 218 / 255)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.h_lines = []
        self.v_lines = []

    def generate_lines(self):

        # HORIZONTAL LINES
        no_h_lines = int(self.height / self.SPACING)
        last_y = 0

        for line in self.h_lines:
            last_y += self.SPACING
            line.points = (0, last_y, self.width, last_y)
        if len(self.h_lines) < no_h_lines:
            with self.canvas:
                Color(0, 0, 0)
                for _ in range(len(self.h_lines), no_h_lines):
                    last_y += self.SPACING
                    self.h_lines.append(Line(points=(0, last_y, self.width, last_y), width=1))

        # VERTICAL LINES        
        no_v_lines = int(self.width / self.SPACING)
        last_x = 0
        for line in self.v_lines:
            last_x += self.SPACING
            line.points = (last_x, 0, last_x, self.height)
        if len(self.v_lines) < no_v_lines:
            with self.canvas:
                Color(0, 0, 0)
                for _ in range(len(self.v_lines), no_v_lines):
                    last_x += self.SPACING
                    self.v_lines.append(Line(points=(last_x, 0, last_x, self.height), width=1))

    def on_size(self, j, h):
        self.generate_lines()


class Renderer(RelativeLayout):
    SPACING = dp(20)
    LINE_COLOR = (242 / 255, 237 / 255, 218 / 255)
    FOCAL_LENGTH = dp(1200)

    def __init__(self, vertex_list=tuple(), edge_list=tuple(), **kw):
        super().__init__(**kw)
        self.h_lines = []
        self.v_lines = []
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        if vertex_list:
            self.compute_projections()

    def blit(self, vertex_list: tuple, edge_list: tuple):
        self.clear_canvas()
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.compute_projections()

    def on_size(self, j, h):
        self.adjust_center()

    def project_vertex(self, vertex, focal_length: int):
        x, y, z = vertex

        x_projected = (x * focal_length) // (z + focal_length)
        y_projected = (y * focal_length) // (z + focal_length)

        return (x_projected, y_projected)

    def compute_projections(self):
        self.projected_line_list = []
        with self.canvas:
            Color(*self.LINE_COLOR)
            for edge in self.edge_list:
                x, y = self.project_vertex(self.vertex_list[edge[0]], self.FOCAL_LENGTH)
                x1, y1 = self.project_vertex(self.vertex_list[edge[1]], self.FOCAL_LENGTH)
                self.projected_line_list.append((Line(points=(x, y, x1, y1), width=1.4), x, y, x1, y1))
            self.adjust_center()

    def adjust_center(self):
        for i in range(len(self.edge_list)):
            line, x, y, x1, y1 = self.projected_line_list[i]
            x += self.center_x
            y += self.center_y
            x1 += self.center_x
            y1 += self.center_y
            line.points = (x, y, x1, y1)

    def clear_canvas(self):
        for i in range(len(self.edge_list)):
            self.canvas.remove(self.projected_line_list[i][0])
        self.projected_line_list = []
        self.edge_list = tuple()
        self.vertex_list = tuple()


class MainLayout(RelativeLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.renderer = Renderer(size_hint=(1, 1))
        self.add_widget(self.renderer)
        self.vertex_set, self.edge_set, self.object_center = cuboid((0, 0, 400), (300, 300, 300))
        Clock.schedule_interval(self.update, .1)

    def update(self, dt):
        # self.renderer.blit(rotateX(self.vertex_set,self.angle%90),self.edge_set)
        # self.vertex_set=rotateX(self.vertex_set,10)
        self.renderer.blit(self.vertex_set, self.edge_set)

    def on_touch_down(self, touch):
        self.previous_touch_pos = touch.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        pmouseX, pmouseY = self.previous_touch_pos
        mouseX, mouseY = touch.pos
        print(mouseX - pmouseX, mouseY - pmouseY)
        self.previous_touch_pos = touch.pos
        self.vertex_set = rotateY(self.vertex_set, mouseX - pmouseX, self.object_center)
        self.vertex_set = rotateX(self.vertex_set, mouseY - pmouseY, self.object_center)
        return super().on_touch_move(touch)


if __name__ == "__main__":
    class MainApp(App):
        def build(self):
            return MainLayout()


    MainApp().run()
