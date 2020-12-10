import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)

import pyaudio
import wave
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
filename = 'init'
p = pyaudio.PyAudio()
stream=p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)


def cb(ch):
    print("Recording wav:"+filename)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    while GPIO.input(channel) == 0:
        data=stream.read(CHUNK)
        wf.writeframes(data)
    print("Finished :b")
    wf.close()


def set_ofilename(file_name):
    global filename
    filename = file_name

try:
    GPIO.add_event_detect(channel, GPIO.RISING, callback=cb, bouncetime=200)
    set_ofilename('button_test.wav')
    print(filename)

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    GPIO.cleanup()
    GPIO.remove_event_detect(channel)
