from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')


import numpy as np
from kivy.uix.widget import Widget
from kivy.base import Builder
from kivy.app import App
from kivy.graphics import Line,Bezier
from kivy.core.audio import SoundLoader
from kivy.properties import Clock
import wave
from time import time

Builder.load_string("""
<LinePlot>
    canvas:
        Rectangle:
            size:self.size
            pos:self.pos
            source:r"D://Users//Dell//Documents//PythonProjects//KIVY//Aria_Math//aria_math_bg.png"
""")


class LinePlot(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_loc="D://Users//Dell//Documents\PythonProjects\KIVY\Aria_Math\C418 - Aria Math (Synthwave).wav"
        self.chunk_size = 1024*3
        self.no_points=200
        self.load_data(file_loc)
        with self.canvas:
            self.plot_line=Line(width=2)
        Clock.schedule_interval(self.compute_next_chunk,.1)
        self.aria_sound = SoundLoader.load(file_loc)
        self.aria_sound.volume = 1
        self.aria_sound.play()
        self.start=time()
        self.total_pull=0
        

    def load_data(self,file_loc):
        self.wav_obj = wave.open(file_loc, 'rb')
        self.sampling_rate=self.wav_obj.getframerate()
        # self.wav_obj.getsampwidth() gives no of bytes per data
        self.freq = np.fft.fftfreq(self.chunk_size)*self.sampling_rate
        self.max_freq_pos=(self.freq.argmax()+1)//4
        self.axis_data=np.zeros((self.max_freq_pos,2),dtype=np.int16)
        self.axis_data[:,0]=self.freq[:self.max_freq_pos]
        self.duration=self.wav_obj.getnframes()/self.wav_obj.getframerate()

    def on_size(self,j,k):
        c=self.freq[:self.max_freq_pos]
        self.axis_data[:,0]=c/c.max()*self.width

    def compute_next_chunk(self,dt):
        time_diff=time()-self.start+.15
        if time_diff>self.duration:
            exit(0)
        expected_pull=int(time_diff*self.sampling_rate)
        frame = self.wav_obj.readframes(expected_pull-self.total_pull)
        self.total_pull=expected_pull
        self.update_axis_2(np.frombuffer(frame, dtype=np.int16))


    def update_axis_2(self,data):
        sp = np.fft.fft(data) 
        y=abs(sp.real[:self.max_freq_pos])
        y=y[:self.max_freq_pos]
        no_points=min(self.no_points,len(y))
        indices=np.round(np.linspace(0, len(y)-1, no_points)).astype(int)
        sample_points=self.axis_data[indices]
        c=np.sqrt(y[indices])
        sample_points[:,1]=c/c.max()*self.height*0.9
        self.plot_line.points=sample_points.reshape(-1).tolist()


if __name__=="__main__":
    class MainApp(App):
        def build(self):
            return LinePlot()

    MainApp().run()





