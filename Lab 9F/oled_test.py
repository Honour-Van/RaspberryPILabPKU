import time
from datetime import datetime
import spidev as SPI
import SSD1306
from PIL import Image # 调用相关库文件
from PIL import ImageDraw
from PIL import ImageFont
RST = 19
DC = 16
bus = 0
device = 0 # 树莓派管脚配置

if __name__ == '__main__':
    disp = SSD1306.SSD1306(rst=RST,dc=DC,spi=SPI.SpiDev(bus,device))
    disp.begin()
    disp.clear()
    disp.display() # 初始化屏幕相关参数及清屏
    # welcome interface
    font = ImageFont.load_default()
    image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
    draw = ImageDraw.Draw(image)
    x = 30; y = 30;
    draw.text((x,y), 'Hello, Pi!!', font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(1)
    del draw

    # counting down
    double11 = datetime(2021, 1, 1)
    try:
        while True:
            image = Image.new('RGB',(disp.width,disp.height),'black').convert('1')
            draw = ImageDraw.Draw(image)
            
            logo = Image.open('/home/pi/pku.png').resize((40,40), Image.ANTIALIAS).convert('1')
            draw.bitmap((0,20), logo, fill = 1)
            draw.text((30, 0), str(double11), font=font, fill=255)
            delta = double11 - datetime.now()
            delta_str = str(delta)
            line1 = delta_str[:delta_str.find(',')]
            line2 = delta_str[delta_str.find(',')+2: delta_str.find('.')]
            if line2[0] != ':':
                draw.text((70, 20), line1, font=font, fill=255)
                draw.text((50, 40), line2 + '  left', font=font, fill=255)
            else:
                line1 = line1[:line1.find('.')]
                draw.text((70, 20), ' Only', font=font, fill=255)
                draw.text((50, 40), line1 + '  left', font=font, fill=255)
            disp.image(image)
            disp.display()
    except KeyboardInterrupt:
        del draw
        pass

