from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget


class WindowManager2(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager2, self).__init__(**kwargs)
        self.transition = NoTransition()
        self.add_widget(Screen7())
        self.add_widget(Screen8())
        self.add_widget(Screen9())
        self.add_widget(Screen10())

    def move(self, i):
        scr = "Screen" + str(i)
        self.switch_to(scr)


class ToolBar(BoxLayout):
    def __init__(self, g, obj, **kwargs):
        super(ToolBar, self).__init__(**kwargs)
        self.object = obj
        self.orientation = "vertical"
        buttons = list()
        self.call = 0
        self.add_widget(Button(text="A", size_hint=(1, .1)))
        inner = GridLayout(cols=10, size_hint=(1, .1))
        self.add_widget(inner)
        for i in range(4):
            buttons.append(Button(text="Screen" + str(i + 7), on_press=self.test))  # lambda a: self.test("fff")
            inner.add_widget(buttons[i])
        self.add_widget(g)

    def test(self, event):
        self.object.parent.current = event.text


class Screen7(Screen):
    def __init__(self, **kwargs):
        super(Screen7, self).__init__(**kwargs)
        self.name = "Screen7"
        tool = ToolBar(Button(text="7"), self)

        self.add_widget(tool)


class Screen8(Screen):
    def __init__(self, **kwargs):
        super(Screen8, self).__init__(**kwargs)
        self.name = "Screen8"
        tool = ToolBar(Button(text="8"), self)
        self.add_widget(tool)


class Screen9(Screen):
    def __init__(self, **kwargs):
        super(Screen9, self).__init__(**kwargs)
        self.name = "Screen9"
        tool = ToolBar(Button(text="9"), self)

        self.add_widget(tool)


class Screen10(Screen):
    def __init__(self, **kwargs):
        super(Screen10, self).__init__(**kwargs)
        self.name = "Screen10"
        tool = ToolBar(Button(text="10"), self)

        self.add_widget(tool)


class WidgetsLayoutExample(GridLayout):
    my_text = StringProperty(str(0))
    text_input_str = StringProperty("   ")
    count = 0
    count_enabled = BooleanProperty(False)

    def on_button_click(self):
        if self.count_enabled:
            self.count += 1
        self.my_text = str(self.count)

    def on_toogle_button_state(self, widget):
        if widget.state == "normal":
            widget.text = "OFF"
            self.count_enabled = False
        else:
            widget.text = "ON"
            self.count_enabled = True

    def on_text_input_validate(self, widget):
        self.text_input_str = widget.text

    #   def on_switch_active(self, widget):
    #      self.should_slide=widget.active

    def on_slider_value(self, widget):
        print(widget.value)


class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(100):
            self.add_widget(Button(text=str(i + 1), size_hint=(None, None), size=(dp(100), dp(100))))


class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=(100, 100, 400, 400), width=2)
            Color(0, 1, 0, 1)
            Line(circle=(100, 100, 50), width=2)
            Line(rectangle=(400, 400, 80, 60), width=3)
            self.rect = Rectangle(pos=(600, 20), size=(80, 60))

    def on_button_click(self):
        sx, sy = self.rect.size
        x, y = self.rect.pos
        w = self.width
        inc = dp(20)
        if x + sx + inc > w:
            inc = w - x - sx
        print(inc)
        x += inc
        self.rect.pos = (x, y)


class TheLabApp(App):
    pass


TheLabApp().run()
