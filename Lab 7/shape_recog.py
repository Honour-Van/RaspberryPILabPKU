#!/bin/python
import cv2
from imutils.video import FPS

cam = cv2.VideoCapture(0)  # 打开摄像头
tracker = cv2.TrackerKCF_create()

initBB = None
fps = None

while True:
    ret, frame = cam.read()  # 获取摄像头数据
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 色彩变换
    blur = cv2.blur(grey, (5, 5))  # 过滤噪声
    circles = cv2.HoughCircles(blur,  # 识别圆形
                               method=cv2.HOUGH_GRADIENT, dp=1, minDist=200,
                               param1=100, param2=33, minRadius=30, maxRadius=175)
    # if circles is not None:  # 识别到圆形
    #     for i in circles[0, :]:  # 画出识别的结果
    #         cv2.circle(frame, (i[0], i[1]), int(i[2]), (0, 255, 0), 2)
    #         cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            # if circles is not None:  # 识别到圆形
            #     target = 0; mindiff = 2147483647
            #     for i in circles[0, :]:  # 画出识别的结果
            #         if abs(i[0] - (x+w//2)) + abs(i[1] - (y+h//2)) < mindiff:
            #             target = i
            #             mindiff = abs(i[0] - (x+w//2)) + abs(i[1] - (y+h//2))
            #     cv2.circle(frame, (target[0], target[1]), int(target[2]), (0, 255, 0))
            #     cv2.circle(frame, (target[0], target[1]), 2, (0, 0, 255), 3)
            cv2.circle(frame, (x + w//2, y + h//2), w//2,(0, 255, 0), 2)
        # update the FPS counter
        fps.update()
        fps.stop()

    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        initBB = cv2.selectROI("Detected", frame, fromCenter=False,
                               showCrosshair=True)
        tracker.init(frame, initBB)
        fps = FPS().start()
    cv2.imshow('Detected', frame)  # 显示识别图像
    if key == ord("q"):  # 等待按键
        break
cv2.destroyAllWindows()  # 关闭窗口
cam.release()  # 释放摄像头
