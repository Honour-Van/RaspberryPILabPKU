from aip import speech
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)

from emo.backend.voice import speech_recog

from os import system
import pyaudio
import wave
CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
vr = '/home/pi/1900012739/emo/assets/'
def get_record(filename):
    # stream initialized here, else eaily overflow
    stream=p.open(format=FORMAT,channels=CHANNELS,
                  rate=RATE,input=True,frames_per_buffer=CHUNK)
    wf = wave.open(vr +'temp.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("Recording wav:"+filename)
    while GPIO.input(channel) == 0:
        data=stream.read(CHUNK, exception_on_overflow = False)
        wf.writeframes(data)
    print("Finished :b")
    wf.close()
    stream.stop_stream()
    stream.close()
    system("ffmpeg -y -i " + vr + "temp.wav -ac 1 -ar 16000 " + vr + "16k.wav")
    speech_recog(filename)
    system('mpg123 calendar.wav')
    print(filename)

def pressToTalk(index):
    try:
        while True:
            if GPIO.input(channel) == 0:
                get_record('/home/pi/1900012739/emo/assets/vol'+str(index)+'.wav')
                index = index + 1
    except KeyboardInterrupt:
        p.terminate()
        GPIO.cleanup()

if __name__ == '__main__':
    pressToTalk(0)