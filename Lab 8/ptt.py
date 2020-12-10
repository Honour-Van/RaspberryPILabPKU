import RPi.GPIO as GPIO
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)

import pyaudio
import wave
CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

index = 0
def get_record(filename):
    global index
    # stream initialized here, else eaily overflow
    stream=p.open(format=FORMAT,channels=CHANNELS,
                  rate=RATE,input=True,frames_per_buffer=CHUNK)
    filename = filename + '.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("Recording wav:"+filename)
    while GPIO.input(channel) == 0:
        data=stream.read(CHUNK)
        wf.writeframes(data)
    print("Finished :b")
    index = index + 1
    wf.close()
    stream.stop_stream()
    stream.close()

record_list = []
def trainDataRecord():
    global record_list
    for i in range(20):
        filename = 'train_data/' + 'train_' + str(i//5+1) + '_' + str(i%5+1)
        record_list.append(filename)

try:
    trainDataRecord()
    while True:
        if GPIO.input(channel) == 0:
            get_record(record_list[index])
        if index > 20:
            break
except KeyboardInterrupt:
    p.terminate()
    GPIO.cleanup()