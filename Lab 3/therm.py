import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, 50)
pwm.start(0)
pwm.ChangeDutyCycle(0)

import glob

if __name__ == "__main__":
    while True:
        for name in glob.glob('/sys/bus/w1/devices/28*'):
            name+='/w1_slave'
            with open(name, 'r') as f:
                contents = f.readlines()
                s = contents[1].find('t=')
                s = s + 2
                temp = int(contents[1][s:]) / 1000
                print('current temperature:', temp)
            if temp > 30:
                pwm.ChangeDutyCycle(100)
            else:
                pwm.ChangeDutyCycle(0)