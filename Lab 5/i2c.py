import smbus
import time # 包含相关库文件
import datetime as dt
address = 0x68
register = 0x00
bus = smbus.SMBus(1) # 初始化i2c Bus

def hex2dec(num):
    return num // 10 * 16 + num % 10
def dec2hex(num):
    return num // 16 * 10 + num % 16

# FixTime 定义为 2019 年 6 月 12 日 18 时
t = str(dt.datetime.now())
print(t)

year = hex2dec(int(t[2:4]))
month = hex2dec(int(t[5:7]))
day = hex2dec(int(t[8:10]))
hour = hex2dec(int(t[11:13]))
minute = hex2dec(int(t[14:16]))
second = hex2dec(int(t[17:19]))

FixTime = [second, minute, hour, 0x04, day, month, year]
# FixTime=[0x00,0x00,0x18,0x03,0x12,0x06,0x19]

print(FixTime)
# 定义时钟操作函数
def ds3231SetTime():
    bus.write_i2c_block_data(address,register,FixTime)
def ds3231ReadTime():
    return bus.read_i2c_block_data(address,register,7);
ds3231SetTime() # 设置时间
print(FixTime)
FixTime = ds3231ReadTime() # 读出时间
print(FixTime)

weekday = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
try:
    while True:
        t = ds3231ReadTime()
        print('%d-%d-%.2d %s %.2d:%.2d:%.2d' % \
            (2000+dec2hex(t[6]),dec2hex(t[5]),\
                dec2hex(t[4]), \
                    weekday[t[3]],dec2hex(t[2]),\
                        dec2hex(t[1]), dec2hex(t[0])))
        time.sleep(1)
except KeyboardInterrupt:
    pass