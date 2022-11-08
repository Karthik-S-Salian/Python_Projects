from random import choice

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout


class Main(RelativeLayout):
    BALL_SPEED = 0.001
    SPEED_INCREMENT = 0.0005

    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.create_ball()

    def create_ball(self):
        self.ball_radius = dp(20)
        with self.canvas:
            Color(1, 1, 1)
            self.ball = Ellipse(size=(self.ball_radius, self.ball_radius))

    def on_size(self, *args):
        self.speed_increment = self.SPEED_INCREMENT * self.width
        self.ball_speed = self.BALL_SPEED * self.width
        self.ball_x_speed = self.ball_speed * choice([1, -1])
        self.ball_y_speed = self.ball_speed * choice([1, -1])
        self.speed = self.BALL_SPEED * self.height
        self.ball.pos = self.center

    def on_parent(self, j, k):
        Clock.schedule_interval(self.update, 1 / 60)

    def on_leave(self, j, k):
        Clock.unschedule(self.update)

    def update(self, dt):
        x, y = self.ball.pos
        w, h = self.ball.size
        c_x = x + self.ball_x_speed + w
        c_y = y + self.ball_y_speed + h
        if c_x > self.width or self.ball_x_speed + x < 0:
            self.ball_y_speed += (self.ball_y_speed / abs(self.ball_y_speed)) * self.speed_increment
            self.ball_x_speed *= -1
        if c_y > self.height or self.ball_y_speed + y < 0:
            self.ball_y_speed += (self.ball_y_speed / abs(self.ball_y_speed)) * self.speed_increment
            self.ball_y_speed *= -1
        self.ball.pos = (x + self.ball_x_speed, y + self.ball_y_speed)


if __name__ == "__main__":
    class BouncingBallApp(App):

        def build(self):
            return Main()

    BouncingBallApp().run()
