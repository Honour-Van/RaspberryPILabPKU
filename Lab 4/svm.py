import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
import numpy as np
import spidev as SPI
import SSD1306
from PIL import Image # 调用相关库文件
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
channel = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN, GPIO.PUD_UP)


digits = datasets.load_digits()
images_and_labels = list(zip(digits.images, digits.target))
for index, (image, label) in enumerate(images_and_labels[:4]):
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Training: %i' % label)
n_samples = len(digits.images)
data = digits.images.reshape((n_samples, -1))
classifier = svm.SVC(kernel = 'rbf', gamma=0.001)
classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])
expected = digits.target[n_samples // 2:]
predicted = classifier.predict(data[n_samples // 2:])
print("Classification report for classifier %s:\n%s\n"% (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
images_and_predictions = list(zip(digits.images[n_samples // 2:], predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)
plt.show()
print('plt has shown')

RST = 19
DC = 16
bus = 0
device = 0 # 树莓派管脚配置
disp = SSD1306.SSD1306(rst=RST,dc=DC,spi=SPI.SpiDev(bus,device))
disp.begin()
disp.clear()
disp.display() # 初始化屏幕相关参数及清屏

cur = 0

def cb(ch):
    global cur
    cur = cur + 1
    if cur >= 4:
        cur = 0
    kk = digits.images
    digit = Image.fromarray((kk[cur+4]*8).astype(np.uint8), mode='L').resize((48,48)).convert('1')
    img = Image.new('1',(disp.width,disp.height),'black')
    img.paste(digit, (0, 16, digit.size[0], digit.size[1]+16))
    disp.clear()
    font = ImageFont.load_default()
    image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
    draw = ImageDraw.Draw(image)
    draw.bitmap((10,0), img, fill = 1)
    draw.text((70,0), "Prediction: ", font=font, fill=255)
    draw.text((90,30), str(predicted[cur]), font=font, fill=255)
    disp.image(image)
    disp.display()

if __name__ == "__main__":
    font = ImageFont.load_default()
    image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
    draw = ImageDraw.Draw(image)
    x = 30; y = 30;
    draw.text((x,y), 'Hello, Pi!!', font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    del draw
    try:
        GPIO.add_event_detect(channel, GPIO.RISING, callback=cb, bouncetime=200)
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
        GPIO.remove_event_detect(channel)
