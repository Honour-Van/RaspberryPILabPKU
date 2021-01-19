import RPi.GPIO as GPIO

channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)

def cb(ch):
    print("KEY PRESSED")
GPIO.add_event_detect(channel, GPIO.RISING, callback=cb, bouncetime=200)