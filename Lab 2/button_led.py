import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, 50)
pwm.start(0)
for dc in range(0, 101, 5):
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.05)
for dc in range(100, -1, -5):
    pwm.ChangeDutyCycle(dc)
    time.sleep(0.05)
print("LED Init...Finished")

channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)
print("button Init...Finished")


cb1_mode = True
def cb1(ch):
    global cb1_mode
    if cb1_mode:
        lighter()
    else:
        darker()
    if cb1_mode:
        cb1_mode = False
    else:
        cb1_mode = True
    # print(cb1_mode)
def lighter():
    print("lighter")
    for dc in range(0, 101, 5):
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.05)
def darker():
    print("darker")
    for dc in range(100, -1, -5):
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.05)
        

def breath_led():
    try:
        GPIO.add_event_detect(channel, GPIO.RISING, \
            callback=cb1, bouncetime=200)
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
        GPIO.remove_event_detect(channel)


if __name__ == "__main__":
    breath_led()
    
    