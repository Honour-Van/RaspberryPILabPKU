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


sleeptime = 0
last_time = 0
cb2_mode = False
def cb2(ch):
    global last_time
    global sleeptime
    global cb2_mode
    if time.time() - last_time > 0.5:
        if cb2_mode == False:
            cb2_mode = True
            sleeptime = 1.6
            print("Twinkle starting...")
        else:
            sleeptime = sleeptime / 2
            print("Freq doubled...")
        if sleeptime < 0.2:
            sleeptime = 0.8
            print("Freq reinit...")
    else:
        cb2_mode = False
        print("Turning down...")
    last_time = time.time()


if __name__ == "__main__":
    global cb2_mode
    try:
        GPIO.add_event_detect(channel, GPIO.RISING, callback=cb2, bouncetime=200)
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
    try:
        while True:
            while cb2_mode:
                pwm.ChangeDutyCycle(0)
                time.sleep(sleeptime)
                pwm.ChangeDutyCycle(100)
                time.sleep(sleeptime)
            while ~cb2_mode:
                pwm.ChangeDutyCycle(0)
                time.sleep(sleeptime)
    except KeyboardInterrupt:
        print("Ending...")
        GPIO.cleanup()
    except:
        print("Unknown error!")
        GPIO.cleanup()