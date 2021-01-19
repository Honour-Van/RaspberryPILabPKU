import RPi.GPIO as GPIO
import numpy as np
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)
LED = 26
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, 50)
pwm.start(0)

m1 = 2
m2 = 1
m3 = 5

alpha = 0.01
w1 = 1
w2 = 1
b = 1
len = 2000
x1 = np.random.rand(len) * 10
x2 = np.random.rand(len) * 10
y = x1 * m1 + x2 * m2 + m3 + np.random.randn(len)
error = 2147483647

def cb(ch):
    epoch()
    
def epoch():
    global w1
    global w2
    global b
    global y
    global x1
    global x2
    global error

    for i in range(len):
        yi = x1[i] * w1 + x2[i] * w2 + b
        d = yi - y[i]
        error = d * d
        if error < 1e-5:
            pwm.ChangeDutyCycle(100)
            break
        diff = [alpha * d * x1[i], alpha * d * x2[i], alpha * d]
        w1 = w1 - diff[0]
        w2 = w2 - diff[1]
        b = b - diff[2]
        print(diff)
    print("one epoch finished")
        
        
if __name__ == "__main__":
    GPIO.add_event_detect(channel, GPIO.RISING, callback=cb, bouncetime=200)
    