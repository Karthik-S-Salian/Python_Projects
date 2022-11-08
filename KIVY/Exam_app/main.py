import re
from collections import namedtuple
from functools import partial

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import Clock, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from exam_handler import ExamHandler

Window.clearcolor = (1, 1, 1, 1)
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

EXAM_OBJECT = ExamHandler()
question_sets = EXAM_OBJECT.data_dict
CURRENT_SET = 1

ColorSchema = namedtuple("ColorSchema", ["NOT_VISITED", "VISITED", "SAVED", "MARKED", "CURRENT"])
DEFAULTCOLOR = ColorSchema((1, 1, 0, .5), (0, 0, 0, 0.5), (0, 1, 0, 1), (1, 0.4, 1, 1), (0, 1, 1, 1))


class ExamStatsGrid(GridLayout):
    pass


class BorderedLabel(Label):
    pass


class BorderedButton(Button):
    pass


class OptionLayout(GridLayout):
    pass


class NumberLabel(Label):
    pass


class QuestionSetButton(Button):
    pass


class FlexBox(RelativeLayout):
    def __init__(self, **kwargs):
        super(FlexBox, self).__init__(**kwargs)

    def on_parent(self, crr_object, parent):
        if self.parent:
            item_count = len(self.children)
            self.offset = .2  # 1 / (item_count + (item_count & 1) * -.5)

            crr = 0.5 - item_count // 2 * self.offset + (not item_count & 1) * self.offset / 2
            for item in self.children:
                item.pos_hint = {"center_x": 0.5, "center_y": crr}
                crr += self.offset


class MenuScreen(Screen):

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.button_names = list(question_sets.keys())
        self.add_buttons()

    def add_buttons(self):
        flex = FlexBox()
        for i, name in enumerate(self.button_names):
            flex.add_widget(Button(text=name,
                                   on_press=self.change_subject,
                                   size_hint=(.30, .1),
                                   background_normal="",
                                   background_color=(230 / 255, 0, 92 / 255)
                                   ))
        flex.add_widget(Button(text="Settings",
                               on_press=self.redirect_setting,
                               size_hint=(.30, .1),
                               background_normal="",
                               background_color=(230 / 255, 0, 92 / 255)
                               ))
        self.add_widget(flex)

    def change_subject(self, obj):
        EXAM_OBJECT.subject = obj.text
        self.manager.current = "selection"

    def redirect_setting(self, obj):
        self.manager.current = "settings"


class QuestionSetSelectionScreen(Screen):
    bg_image = StringProperty("")

    def __init__(self, **kwargs):
        super(QuestionSetSelectionScreen, self).__init__(**kwargs)

    def add_buttons(self, subject):
        self.container = GridLayout(cols=2, size_hint=(1, 1))
        inlayout1 = GridLayout(cols=1, size_hint=(.1, 1))
        inlayout2 = GridLayout(cols=1, size_hint=(1, 1))
        inlayout1.add_widget(
            Button(text="<", on_press=self.back, size_hint=(1, .13), background_normal="", color=(0, 0, 0),
                   font_size=dp(25)))
        inlayout2.add_widget(
            Label(text="available question sets", color=(0, 0, 0), size_hint=(1, .13), font_size=dp(20)))
        button_names = question_sets[subject]["question_sets"]
        for i, name in enumerate(button_names):
            inlayout1.add_widget(NumberLabel(text=str(i + 1)))
            inlayout2.add_widget(QuestionSetButton(text=re.findall(r'[^\\/]+?(?=\.\w+$)', str(name))[0],
                                                   on_press=partial(self.select_question_set, i)))
        inlayout1.add_widget(Label())
        inlayout2.add_widget(Label())
        self.container.add_widget(inlayout1)
        self.container.add_widget(inlayout2)
        self.add_widget(self.container)

    def back(self, obj):
        self.manager.current = "menu"

    def on_parent(self, j, k):
        if self.manager.current == self.name:
            self.add_buttons(EXAM_OBJECT.subject)
            self.bg_image = str(question_sets[EXAM_OBJECT.subject]['bg_image'])

    def select_question_set(self, value, obj):
        EXAM_OBJECT.question_set_index = value
        EXAM_OBJECT.topic = obj.text
        self.manager.current = "startexam"

    def on_leave(self):
        self.remove_widget(self.container)


class ExamScreenLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(ExamScreenLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.heading = Label(size_hint=(1, None), height=dp(50), color=(0, 0, 0, 1))
        self.add_widget(self.heading)
        self.navigator = QuestionNavigator()
        self.question_layout = QuestionsLayout()
        self.exam_stats_grid = ExamStatsGrid()
        self.navigator.question_layout = self.question_layout
        self.question_layout.navigator = self.navigator
        self.add_widget(self.exam_stats_grid)
        self.add_widget(self.navigator)
        self.exam_stats_layout()
        self.add_widget(self.question_layout)

    def exam_stats_layout(self):
        self.question_attempted_label = self.exam_stats_grid.ids["Label1"]
        self.question_remain_label = self.exam_stats_grid.ids["Label3"]
        self.time_label = self.exam_stats_grid.ids["Label2"]

    def update_topic(self):
        self.heading.text = EXAM_OBJECT.topic



class PopupLayout(Popup):
    def __init__(self, obj, **kwargs):
        super(PopupLayout, self).__init__(**kwargs)
        self.obj = obj
        self.size_hint = (.4, .3)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.title = "!! WARNING !!"
        self.title_align = "center"
        self.title_color = (1, 0, 0, 1)
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Really want to cancel the exam"))
        button_layout = BoxLayout(size_hint=(1, 0.3))
        button_layout.add_widget(Button(text="Yes", on_release=self.cancel_exam))
        button_layout.add_widget(Button(text="cancel", on_release=self.dismiss))
        layout.add_widget(button_layout)
        self.content = layout

    def cancel_exam(self, c):
        self.dismiss()
        self.obj.manager.current = "menu"
        EXAM_OBJECT.reset()


class QuestionNavigator(ScrollView):
    BUTTON_WIDTH = 80
    question_layout = ObjectProperty()

    def __init__(self, **kwargs):
        super(QuestionNavigator, self).__init__(**kwargs)
        self.question_layout = None
        self.layout = BoxLayout(size_hint_x=None, width=80 * 40)
        self.buttons = []
        for i in range(1, 41):
            b = Button(text=str(i), on_press=self.button_fun, size_hint=(None, .9), width=self.BUTTON_WIDTH,
                       pos_hint={"center_y": .5})
            b.background_color = DEFAULTCOLOR.NOT_VISITED
            self.buttons.append(b)
            self.layout.add_widget(b)

        self.add_widget(self.layout)

    def shift_scroll(self, current):
        self.scroll_x = current * (1 / 40)

    def button_fun(self, obj):
        self.question_layout.on_change(int(obj.text))

    def change_button_color(self, color, index):
        self.buttons[index].background_color = color


class QuestionsLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(QuestionsLayout, self).__init__(size_hint=(1, .5), orientation="vertical", **kwargs)
        self.question_label = Label(pos_hint={"x": 0.03, "y": 0.02}, text="", size_hint=(1, 0.3), color=(0, 0, 0, 1,),
                                    font_size=dp(19))
        self.add_widget(self.question_label)
        self.navigator = None
        self.optionlayout = OptionLayout()
        self.add_widget(self.optionlayout)
        self.current = 0
        self.add_widget(Label(size_hint_y=.1))
        self.active_box = None
        self.button_color = DEFAULTCOLOR.VISITED
        self.is_marked = False
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_up=self.on_keyboard_up)
        self.keyboard = None

    def on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'left':
            self.shift_question(-1)
        if keycode[1] == 'right':
            self.shift_question(1)

    def on_size(self, parent, root):
        self.question_label.size = self.parent.width, self.height * .3
        self.question_label.text_size = self.question_label.size
        self.question_label.halign = "left"
        self.question_label.valign = "middle"
        self.question_label.padding = dp(15), dp(5)
        self.question_label.max_lines = 5

    def on_screen_change(self, screen):
        if screen.manager.current == screen.name:
            self.keyboard.bind(on_key_up=self.on_keyboard_up)
            if not EXAM_OBJECT.has_started:
                self.current = 0
                self.navigator.shift_scroll(self.current)
                self.exam_object = EXAM_OBJECT
                self.exam_object.start_session(int(CURRENT_SET))
                self.on_change(1)
                self.timer_schedule = Clock.schedule_interval(self.update, 1)
        else:
            self.keyboard.unbind(on_key_up=self.on_keyboard_up)

    def update(self, dt):
        if EXAM_OBJECT.has_started:
            min, sec = self.exam_object.get_time()
            self.parent.time_label.text = str(min) + " : " + str(sec)
            if min + sec == 0:
                Clock.unschedule(self.update)
                EXAM_OBJECT.end_session()
                self.parent.parent.manager.current = "result"
        else:
            Clock.unschedule(self.update)

    def shift_question(self, shift):
        if 0 <= self.current + shift < 40:
            self.on_change(self.current + 1 + shift)
            self.navigator.shift_scroll(self.current + 1)

    def on_change(self, value):
        self.navigator.change_button_color(self.button_color, self.current)
        self.button_color = DEFAULTCOLOR.VISITED
        if self.active_box:
            self.optionlayout.ids["checkbox" + str(self.active_box)].active = False
        self.current = value - 1
        self.navigator.change_button_color(DEFAULTCOLOR.CURRENT, self.current)
        ques, options, selected, self.is_marked = self.exam_object.get_current_question(self.current)
        self.question_label.text = str(value) + ") " + ques
        self.optionlayout.ids["option_1"].text = options[0]
        self.optionlayout.ids["option_2"].text = options[1]
        self.optionlayout.ids["option_3"].text = options[2]
        self.optionlayout.ids["option_4"].text = options[3]

        if not selected is None:
            selected += 1
            self.active_box = selected
            self.optionlayout.ids["checkbox" + str(selected)].active = True

    def checkbox_click(self, is_active, value):
        self.active_box = value
        if is_active:
            self.exam_object.change_selection(value - 1)
            self.parent.question_attempted_label.text = str(self.exam_object.no_attempted_q)
            self.parent.question_remain_label.text = str(self.exam_object.remaining_q)
            if not self.is_marked:
                self.button_color = (0, 1, 0, 1)
                self.navigator.change_button_color(self.button_color, self.current)

    def clear_selection(self):
        if self.active_box:
            self.exam_object.clear_selection()
            self.optionlayout.ids["checkbox" + str(self.active_box)].active = False
            self.active_box = None
            if not self.is_marked:
                self.button_color = DEFAULTCOLOR.VISITED
                self.navigator.change_button_color(self.button_color, self.current)

    def mark_review(self):
        state = self.exam_object.change_review_state()
        if state[0]:
            self.button_color = DEFAULTCOLOR.MARKED
            self.is_marked = True
            self.navigator.change_button_color(self.button_color, self.current)
        elif state[1]:
            self.is_marked = False
            self.button_color = DEFAULTCOLOR.VISITED
            self.navigator.change_button_color(self.button_color, self.current)
        else:
            self.button_color = DEFAULTCOLOR.SAVED
            self.is_marked = False
            self.navigator.change_button_color(self.button_color, self.current)


class QuestionStatsLayout(GridLayout):
    def __init__(self, **kwargs):
        super(QuestionStatsLayout, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(BorderedLabel(text="Questions Attempted", ))
        self.attempted_label = BorderedLabel()
        self.add_widget(self.attempted_label)
        self.add_widget(BorderedLabel(text="Remaining Questions"))
        self.remaining_label = BorderedLabel()
        self.add_widget(self.remaining_label)
        self.add_widget(BorderedLabel(text="Marked as review Questions", ))
        self.marked_label = BorderedLabel(text="0")
        self.add_widget(self.marked_label)
        self.add_widget(BorderedLabel(text="time remaining"))
        self.time_label = BorderedLabel()
        self.add_widget(self.time_label)

    def on_screen_change(self, screen):
        if screen.manager.current == screen.name:
            self.attempted_label.text = str(EXAM_OBJECT.no_attempted_q)
            self.remaining_label.text = str(EXAM_OBJECT.remaining_q)
            self.marked_label = str(EXAM_OBJECT.no_marked)
            Clock.schedule_interval(self.update, 1)

    def update(self, dt):
        min, sec = EXAM_OBJECT.get_time()
        self.time_label.text = str(min) + " : " + str(sec)

    def end_exam(self):
        EXAM_OBJECT.end_session()
        Clock.unschedule(self.update)


class ResultLayout(GridLayout):
    def __init__(self, **kwargs):
        super(ResultLayout, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(BorderedLabel(text="Total no of Questions"))
        self.add_widget(BorderedLabel(text="40"))
        self.add_widget(BorderedLabel(text="topic"))
        self.topic_label = BorderedLabel()
        self.add_widget(self.topic_label)
        self.add_widget(BorderedLabel(text="Marks Obtained"))
        self.mark_label = BorderedLabel()
        self.add_widget(self.mark_label)
        self.add_widget(BorderedLabel(text="time taken"))
        self.time_label = BorderedLabel()
        self.add_widget(self.time_label)

    def on_screen_change(self, screen):
        if screen.manager.current == screen.name:
            self.mark_label.text = str(EXAM_OBJECT.mark)
            self.topic_label.text = EXAM_OBJECT.topic
            c = EXAM_OBJECT.stop_time
            self.time_label.text = str(c.tm_min) + " : " + str(c.tm_sec)

    def on_leave(self):
        EXAM_OBJECT.reset()


if __name__ == "__main__":
    class MainApp(App):
        pass


    MainApp().run()
