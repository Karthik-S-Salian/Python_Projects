import pyaudio
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
from time import time

plt.ion()

def plot(x,y):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Frequency Analysis')
    plt.xlabel('Frequencies')
    plt.ylabel('Amplitude')
    plt.plot(x,y)
    plt.ylim(ymin=0)
    plt.xlim((0,5000))
    plt.show(block=False)
    plt.pause(10)

def extract_frequency_data(data):
    t = np.arange(data.shape[0])
    freq = np.fft.fftfreq(data.shape[0])*RATE
    sp = np.fft.fft(data) 
    plot(freq,abs(sp.real))
    print(freq,abs(sp.real))
    exit(0)



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS=1
RATE=44100

p=pyaudio.PyAudio()

stream = p.open(rate=RATE,
    channels=CHANNELS,
    format=FORMAT,
    input=True,
    frames_per_buffer=CHUNK,
    start=False)


frames=[]
seconds=CHUNK/RATE*200

stream.start_stream()
start=time()

for i in range(0,int(RATE/CHUNK*seconds)):
    data=stream.read(CHUNK)
    
    y = np.frombuffer(data, dtype=np.int16)
    extract_frequency_data(y)


print(time()-start)
stream.stop_stream()
stream.close()
p.terminate()



