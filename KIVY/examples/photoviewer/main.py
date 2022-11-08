import kivy
from kivy.uix.screenmanager import Screen

kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty


class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)


class MinScreen(Screen):
    def __init__(self,**kwargs):
        super(MinScreen, self).__init__(**kwargs)

        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'data/images', '*')):
            try:
                # load the image

                picture = Picture(source=filename, rotation=randint(-30, 30))
                print(type(picture))
                # add to the main field
                self.add_widget(picture)
            except Exception as e:
                print(e)
                # Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True


class PicturesApp(App):

    def build(self):
        return MinScreen()




if __name__ == '__main__':
    PicturesApp().run()
