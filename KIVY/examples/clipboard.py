from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.button import Button


Builder.load_string("""
#:import Clipboard kivy.core.clipboard.Clipboard
#:import Clock kivy.clock.Clock
<MyGrid>:
    cols: 1
    BoxLayout:
        Button:
            padding:[]
            text: 'Copy'
            on_release:
                Clipboard.copy(txtinput.text)
        Button:
            text: 'Paste'
            on_release:
                txtinput.text = Clipboard.paste()
    TextInput:
        id: txtinput
        on_focus: Clock.schedule_once(lambda dt: self.select_all(),0.25) if self.focus else None
""")

class MyGrid(GridLayout):
    pass

class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()