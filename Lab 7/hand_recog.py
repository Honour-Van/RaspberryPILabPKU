import numpy as np
import cv2
import imutils
cam = cv2.VideoCapture(0) # 初始化摄像头

def nothing(sth):
    pass
cv2.namedWindow('Area Control Panel')
cv2.createTrackbar('area: min', 'Area Control Panel', 10000, 150000, nothing)
cv2.createTrackbar('area: max', 'Area Control Panel', 150000, 150000, nothing)

cv2.namedWindow('Color Control Panel')
cv2.createTrackbar('H:min', 'Color Control Panel', 0, 180, nothing)
cv2.createTrackbar('H:max', 'Color Control Panel', 180, 180, nothing)
cv2.createTrackbar('S:min', 'Color Control Panel', 0, 255, nothing)
cv2.createTrackbar('S:max', 'Color Control Panel', 255, 255, nothing)
cv2.createTrackbar('V:min', 'Color Control Panel', 0, 255, nothing)
cv2.createTrackbar('V:max', 'Color Control Panel', 255, 255, nothing)


while ( True ):
    ret, frame = cam.read() # 读取摄像头数据
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # 转换颜色空间
    # 通过颜色设计模板
    hl = cv2.getTrackbarPos('H:min', 'Color Control Panel')
    hh = cv2.getTrackbarPos('H:max', 'Color Control Panel')
    sl = cv2.getTrackbarPos('S:min', 'Color Control Panel')
    sh = cv2.getTrackbarPos('S:max', 'Color Control Panel')
    vl = cv2.getTrackbarPos('V:min', 'Color Control Panel')
    vh = cv2.getTrackbarPos('V:max', 'Color Control Panel')
    image_mask=cv2.inRange(hsv,np.array([hl, sl, vl]), np.array([hh, sh, vh]))
    
    # 计算输出图像
    output=cv2.bitwise_and(frame,frame,mask=image_mask)
            
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # 注意，在应用阈值化之后，形状是如何在黑色背景上表示为白色前景。
    # 下一步是使用轮廓检测​​找到这些白色区域的位置：
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    area_l = cv2.getTrackbarPos('area: min', 'Area Control Panel')
    area_h = cv2.getTrackbarPos('area: max', 'Area Control Panel')
    # 遍历轮廓集
    for c in cnts:
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。这些力矩捕获了形状的基本统计特性，包括对象的面积，质心（即，对象的中心（x，y）坐标），方向以及其他所需的特性。
        M = cv2.moments(c)
        area = M["m00"]
        if area > area_h or area < area_l:
            continue
        if M["m00"] == 0:
            M["m00"] = 0.001
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 在图像上绘制轮廓及中心
        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('Original',frame) # 显示原始图像
    cv2.imshow('Output',output) # 显示输出图像
    if cv2.waitKey(1) == ord("q"): # 等待按键
        break
cam.release()
cv2.destroyAllWindows()
