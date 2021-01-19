import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

def output_twinkle():
    try:
        while True:
            GPIO.output(LED, 1)
            time.sleep(0.2)
            GPIO.output(LED, 0)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Ending...")
        GPIO.cleanup()
    except:
        print("Unknown error!")
        GPIO.cleanup()

def pwm_twinkle():
    pwm = GPIO.PWM(LED, 50)
    pwm.start(0)
    try:
        while True:
            pwm.ChangeDutyCycle(100)
            time.sleep(0.2)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Ending...")
        pwm.stop()
        GPIO.cleanup()
    except:
        print("Unknown error!")
        pwm.stop()
        GPIO.cleanup()



if __name__ == "__main__":
    output_twinkle()
    #pwm_twinkle()