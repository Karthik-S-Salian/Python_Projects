from kivy.app import App
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout


class FlexBox(RelativeLayout):
    orientation = StringProperty("vertical")
    offset = BoundedNumericProperty(0, min=0, max=1)
    halign = BoundedNumericProperty(0.5, min=0, max=1)

    def __init__(self,orientation="vertical",**kwargs):
        super(FlexBox, self).__init__(**kwargs)
        self.orientation=orientation

    def on_children(self,crr_object, children):
        if self.parent:
            item_count = len(children)
            self.offset = 1 / (item_count+(item_count & 1)*-.5)

            crr = 0.5 - item_count // 2 * self.offset + (not item_count & 1) * self.offset / 2
            for item in children:
                item.pos_hint = {"center_x": self.halign, "center_y": crr}
                crr += self.offset
            print("here")

    def on_parent(self,crr_object, parent):
        if parent:
            self.on_children(self,self.children)





class testbox(BoxLayout):

    def __init__(self,**kwargs):
        super(testbox, self).__init__(**kwargs)
        self.orientation="vertical"
        self.spacing=dp(20)
        b1=Button(text="cwfc",size_hint=(None,None),size=(dp(200),dp(100)))
        b2=Button(text="cwfc",size_hint=(None,None),size=(dp(200),dp(100)))
        b3=Button(text="cwfc",size_hint=(None,None),size=(dp(200),dp(100)))

        b4=Button(text="cwfc",size_hint=(None,None),size=(dp(200),dp(100)))
        self.add_widget(b1)
        self.add_widget(b2)
        self.add_widget(b3)
        self.add_widget(b4)
        self.add_widget(Button())




if __name__=="__main__":
    class tesst(FlexBox):
        def __init__(self,**kwargs):
            super(tesst, self).__init__(offset=.2,**kwargs)
            self.add_widget(Button(text="d",size_hint=(.5,.1)))
            self.add_widget(Button(text="w",size_hint=(.5,.1)))
            self.add_widget(Button(text="s",size_hint=(.5,.1)))
            self.add_widget(Button(text="r", size_hint=(1, .1)))
            self.add_widget(Button(text="p", size_hint=(1, .1)))

    class TextApp(App):
        def build(self):
            return  testbox()

    TextApp().run()

