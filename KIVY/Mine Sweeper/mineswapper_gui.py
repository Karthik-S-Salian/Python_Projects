from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout


class MainWidget(RelativeLayout):
    def __init__(self,**kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_board(5)


    def init_board(self,size):
        layout=StackLayout()
        layout.orientation= "lr-tb"
        for i in range(size*size):
            l=Button(text=str(i+1),size_hint=(.1,.1))
            layout.add_widget(l)
        self.add_widget(layout)





if __name__=="__main__":
    class Main_App(App):
        pass

    Main_App().run()