from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.base import Builder

import os

kv_str="""
<Root>:
    text_input: text_input

    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: 'Load'
                on_release: root.show_load()
            Button:
                text: 'Save'
                on_release: root.show_save()

        BoxLayout:
            TextInput:
                id: text_input
                text: ''

            RstDocument:
                text: text_input.text
                show_errors: True

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserIconView:
            filters:["*.png","*.jpg"]
            id: filechooser
            path:"D:/"

        RelativeLayout:
            size_hint_y: None
            height: 30
            Label:
                size_hint:None,0.9
                width:dp(70)
                pos_hint:{"right":0.35,"center_y":0.5}
                text:"File Name:"
            Label:
                size_hint:.34,0.9
                text:""
                pos_hint:{"x":0.36,"center_y":0.5}
                canvas:
                    Color:
                        rgb: 1,1,1
                    Line:
                        width: 1
                        rectangle: self.x, self.y, self.width, self.height
            RelativeLayout:
                size_hint:None,0.9
                width:dp(200)
                pos_hint:{"right":0.99,"center_y":0.5}
                Button:
                    text: "Open"
                    size_hint:.4,1
                    width:dp(90)
                    pos_hint:{"x":0.05,"center_y":0.5}
                    canvas:
                        Color:
                            rgb: 1,1,1
                        Line:
                            width: 1
                            rectangle: self.x, self.y, self.width, self.height
                    on_release: root.load(filechooser.path, filechooser.selection)
                Button:
                    canvas:
                        Color:
                            rgb: 1,1,1
                        Line:
                            width: 1
                            rectangle: self.x, self.y, self.width, self.height
                    text: "Cancel"
                    size_hint:.4,1
                    width:dp(90)
                    pos_hint:{"right":.95,"center_y":0.5}
                    on_release: root.cancel()

<SaveDialog>:
    text_input: text_input
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            on_selection: text_input.text = self.selection and self.selection[0] or ''

        TextInput:
            id: text_input
            size_hint_y: None
            height: 30
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Save"
                on_release: root.save(filechooser.path, text_input.text)
"""


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()



if __name__ == '__main__':
    Builder.load_string(kv_str)


    class Editor(App):
    
        def build(self):
            return Root()

    Editor().run()