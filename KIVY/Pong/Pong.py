from random import choice

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Ellipse
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '600')


class EnhancedLabel(Label):
    pass


class GameWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.left_label = EnhancedLabel(color=(0, 1, 0))

        self.right_label = EnhancedLabel(color=(0, 1, 0))
        self.label_layout = BoxLayout(size_hint=(1, .1))
        self.label_layout.add_widget(self.left_label)
        self.label_layout.add_widget(self.right_label)
        self.button_layout = BoxLayout(size_hint=(1, .1))
        self.button_reset = Button(text="restart")
        self.button_start = Button(text="start")
        self.button_layout.add_widget(self.button_reset)
        self.button_layout.add_widget(self.button_start)
        self.add_widget(GameField(self.left_label, self.right_label, self.button_reset, self.button_start))
        self.add_widget(self.label_layout)
        self.add_widget(self.button_layout)


class GameField(RelativeLayout):
    BALL_SPEED = 0.001
    SPEED_INCREMENT = 0.0005
    PADDLE_SPEED = 0.1
    PADDLE_HEIGHT = 0.3
    PADDLE_WIDTH = 0.03

    def __init__(self, label_left, label_right, button_reset, button_start, **kwargs):
        super(GameField, self).__init__(**kwargs)
        self.ball_radius = dp(20)
        self.left_label = label_left
        self.right_label = label_right
        self.reset_button = button_reset
        self.start_button = button_start
        self.start_button.bind(on_press=self.start_or_pause)
        self.reset_button.bind(on_press=self.reset)
        with self.canvas:
            Color(1, 1, 1)
            self.ball = Ellipse(size=(self.ball_radius, self.ball_radius))
        self.paddle_width = 0
        self.paddle_height = 0
        self.ball_x = 0
        self.ball_y = 0
        self.is_running = False
        self.is_pause = False
        self.left_label.text = '0'
        self.right_label.text = '0'
        self.score_left = 0
        self.score_right = 0
        self.paddle_speed = 0
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard.unbind(on_key_up=self.on_keyboard_up)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            if self.right_paddle_y + self.paddle_height < self.height:
                self.right_paddle_y += self.paddle_speed
                self.right_paddle.pos = (self.right_paddle_x, self.right_paddle_y)
        elif keycode[1] == 'down':
            if self.right_paddle_y > 0:
                self.right_paddle_y -= self.paddle_speed
                self.right_paddle.pos = (self.right_paddle_x, self.right_paddle_y)

        if keycode[1] == 'w':
            if self.left_paddle_y + self.paddle_height < self.height:
                self.left_paddle_y += self.paddle_speed
                self.left_paddle.pos = (self.left_paddle_x, self.left_paddle_y)
        elif keycode[1] == 's':
            if self.left_paddle_y > 0:
                self.left_paddle_y -= self.paddle_speed
                self.left_paddle.pos = (self.left_paddle_x, self.left_paddle_y)

    def create_ball(self):
        self.ball_x_speed = self.ball_speed * choice([1, -1])
        self.ball_y_speed = self.ball_speed * choice([1, -1])
        self.ball.pos = self.center
        self.ball_x, self.ball_y = self.center

    def on_size(self, *args):
        self.speed_increment = self.SPEED_INCREMENT * self.width
        self.ball_speed = self.BALL_SPEED * self.width
        self.ball_x_speed = self.ball_speed
        self.ball_y_speed = self.ball_speed
        self.speed = self.BALL_SPEED * self.height
        self.ball.pos = self.center
        self.ball_x, self.ball_y = self.center
        self.resize_paddle()

    def resize_paddle(self):
        self.paddle_height = self.PADDLE_HEIGHT * self.height
        self.paddle_speed = self.PADDLE_SPEED * self.height
        self.paddle_width = self.PADDLE_WIDTH * self.width
        self.left_paddle_x = 0
        self.right_paddle_x = self.width - self.paddle_width
        self.left_paddle_y = self.right_paddle_y = self.center[1] - self.paddle_height / 2
        self.right_paddle.size = (self.paddle_width, self.paddle_height)
        self.left_paddle.size = (self.paddle_width, self.paddle_height)
        self.left_paddle.pos = (self.left_paddle_x, self.left_paddle_y)
        self.right_paddle.pos = (self.right_paddle_x, self.right_paddle_y)

    def create_paddle(self):
        with self.canvas:
            Color(0, 0, 255)
            self.left_paddle = Rectangle()
            Color(255, 0, 0)
            self.right_paddle = Rectangle()

    def on_parent(self, m, n):
        self.create_paddle()

    def update(self, dt):
        self.ball_x += self.ball_x_speed
        self.ball_y += self.ball_y_speed
        if self.ball_y + self.ball_radius >= self.height or self.ball_y <= 0:
            self.ball_y_speed *= -1
            self.ball_y += self.ball_y_speed

        if self.ball_x <= self.paddle_width:
            if self.left_paddle_y < self.ball_y < self.left_paddle_y + self.paddle_height:
                self.ball_x_speed -= self.speed_increment
                self.ball_x_speed *= -1
                self.ball_y_speed += (self.ball_y_speed / abs(self.ball_y_speed)) * self.speed_increment
                self.ball_x = self.paddle_width
            if self.ball_x <= 0:
                self.create_ball()
                self.score_right += 1
                self.right_label.text = str(self.score_right)

        elif self.ball_x + self.ball_radius >= self.width - self.paddle_width:
            if self.right_paddle_y < self.ball_y < self.right_paddle_y + self.paddle_height:
                self.ball_x_speed += self.speed_increment
                self.ball_x_speed *= -1
                self.ball_y_speed += (self.ball_y_speed / abs(self.ball_y_speed)) * self.speed_increment
                self.ball_x = self.width - self.paddle_width - self.ball_radius

            if self.ball_x + self.ball_radius >= self.width:
                self.create_ball()
                self.score_left += 1
                self.left_label.text = str(self.score_left)

        self.ball.pos = (self.ball_x, self.ball_y)

    def start_or_pause(self, btn_obj):
        if not self.is_running:
            Clock.schedule_interval(self.update, 1 / 59)
            self.is_running = True
            btn_obj.text = "PAUSE"
        elif self.is_pause:
            self.is_pause = False
            btn_obj.text = "PAUSE"
            Clock.schedule_interval(self.update, 1 / 59)
        else:
            btn_obj.text = "RESUME"
            self.is_pause = True
            Clock.unschedule(self.update)

    def reset(self, btn):
        self.score_left = self.score_right = 0
        self.ball.pos = self.center
        self.ball_x, ball_y = self.center
        self.left_paddle_y = self.right_paddle_y = self.center[1] - self.paddle_height / 2
        self.left_paddle.pos = (self.left_paddle_x, self.left_paddle_y)
        self.right_paddle.pos = (self.right_paddle_x, self.right_paddle_y)
        Clock.unschedule(self.update)
        self.is_running = False
        self.is_pause = False
        self.left_label.text = '0'
        self.right_label.text = '0'
        self.start_button.text = "START"


def main():
    class PongApp(App):
        def build(self):
            return GameWindow()

    PongApp().run()


if __name__ == "__main__":
    main()
