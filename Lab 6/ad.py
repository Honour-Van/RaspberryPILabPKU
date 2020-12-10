import smbus
import time

import spidev as SPI
import SSD1306
from PIL import Image # 调用相关库文件
from PIL import ImageDraw
from PIL import ImageFont
RST = 19
DC = 16
bus = 0
device = 0 # 树莓派管脚配置

disp = SSD1306.SSD1306(rst=RST,dc=DC,spi=SPI.SpiDev(bus,device))
disp.begin()
disp.clear()
disp.display() # 初始化屏幕相关参数及清屏
font = ImageFont.load_default()
image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
draw = ImageDraw.Draw(image)
x = 30; y = 30;
draw.text((x,y), 'Hello, Pi!!', font=font, fill=255)
disp.image(image)
disp.display()
time.sleep(1)
disp.clear()
disp.display() # 初始化屏幕相关参数及清屏

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)
while True:
    bus.write_byte(address, A0)
    value = bus.read_byte(address)
    voltage = value / 256 * 3.3
    font = ImageFont.load_default()
    image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
    draw = ImageDraw.Draw(image)
    x = 30; y = 30;
    draw.text((x,y), 'Voltage: %.4f'%voltage, font=font, fill=255)
    disp.image(image)
    disp.display()
    print(voltage)