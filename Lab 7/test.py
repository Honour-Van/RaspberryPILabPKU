# !/bin/python3
# 采用第 7.2.2 节中的代码对摄像头进行测试
import cv2 # 加载 OpenCV 库
cam = cv2.VideoCapture(0) # 打开摄像头
cam.set(3, 1024) # 设置图像宽度
cam.set(4, 768) # 设置图像高度
def cam_clear():
    cam.release() # 释放摄像头硬件
    cv2.destroyAllWindows() # 关闭全部窗口
try:
    while(True):
        ret, frame = cam.read() # 读入一帧图像
        cv2.imshow('Video Test',frame) # 显示图像
        if cv2.waitKey(1) == ord("q") : # 等待按键
            cam_clear()
            break
except KeyboardInterrupt:
    cam_clear()