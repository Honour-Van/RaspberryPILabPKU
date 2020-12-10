import numpy as np
import cv2
cam = cv2.VideoCapture(0)  # 初始化摄像头

# create trackbars for color change


def nothing(sth):
    pass
cv2.namedWindow('Control Panel')
cv2.createTrackbar('H:min', 'Control Panel', 0, 180, nothing)
cv2.createTrackbar('H:max', 'Control Panel', 180, 180, nothing)
cv2.createTrackbar('S:min', 'Control Panel', 0, 255, nothing)
cv2.createTrackbar('S:max', 'Control Panel', 255, 255, nothing)
cv2.createTrackbar('V:min', 'Control Panel', 0, 255, nothing)
cv2.createTrackbar('V:max', 'Control Panel', 255, 255, nothing)

while (True):
    ret, frame = cam.read()  # 读取摄像头数据
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换颜色空间
    # 通过颜色设计模板
    hl = cv2.getTrackbarPos('H:min', 'Control Panel')
    hh = cv2.getTrackbarPos('H:max', 'Control Panel')
    sl = cv2.getTrackbarPos('S:min', 'Control Panel')
    sh = cv2.getTrackbarPos('S:max', 'Control Panel')
    vl = cv2.getTrackbarPos('V:min', 'Control Panel')
    vh = cv2.getTrackbarPos('V:max', 'Control Panel')
    image_mask = cv2.inRange(hsv, np.array(
        [hl, sl, vl]), np.array([hh, sh, vh]))
    # 计算输出图像
    output = cv2.bitwise_and(frame, frame, mask=image_mask)
    cv2.imshow('Original', frame)  # 显示原始图像
    cv2.imshow('Output', output)  # 显示输出图像
    if cv2.waitKey(1) == ord("q"):  # 等待按键
        break
cam.release()
cv2.destroyAllWindows()
