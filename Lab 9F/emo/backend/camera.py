from ..backend.voice import tts
from threading import Thread
from os import system
import cv2

from ..backend.image import resize_image, convert_color_space, show_image
from ..backend.image import BGR2RGB

import spidev as SPI
import SSD1306
from PIL import Image  # 调用相关库文件
from PIL import ImageDraw
RST = 19
DC = 16
bus = 0
device = 0  # 树莓派管脚配置

emotion = 'happy'
value = 1

readyToPlay = False
recordNum = 0


def playCalendar():
    vr = '/home/pi/1900012739/emo/assets/'  # voice root
    global recordNum
    global readyToPlay
    while True:
        if readyToPlay:
            system("mpg123 " + vr + "calendar.wav")
            mode = input('[calendar]想听听今天的日程嘛？(1是 (default)否)')
            if mode:
                for i in range(recordNum):
                    system('mpg123 ' + vr + 'vol'+str(i+1)+'.wav')
                readyToPlay = False
            else:
                pass


def expression(emotion):  # (str)emotion
    disp = SSD1306.SSD1306(rst=RST, dc=DC, spi=SPI.SpiDev(bus, device))
    disp.begin()
    disp.clear()
    disp.display()  # 初始化屏幕相关参数及清屏
    image = Image.new('RGB', (disp.width, disp.height), 'black').convert('1')
    draw = ImageDraw.Draw(image)
    ir = '/home/pi/1900012739/emo/assets/'  # image root
    expression = Image.open(
        ir + 'saucer-eye.png').resize((50, 50), Image.ANTIALIAS).convert('1')
    global readyToPlay
    if emotion == 'neutral':
        readyToPlay = True
    elif emotion == 'happy':
        expression = Image.open(
            ir + 'happy.png').resize((50, 50), Image.ANTIALIAS).convert('1')
        readyToPlay = True
    elif emotion == 'angry':
        expression = Image.open(
            ir + 'pitiful.png').resize((50, 50), Image.ANTIALIAS).convert('1')
    elif emotion == 'sad':
        expression == Image.open(
            ir + 'comforting.png').resize((50, 50), Image.ANTIALIAS).convert('1')
    elif emotion == 'fear':
        expression == Image.open(
            ir + 'comforting.png').resize((50, 50), Image.ANTIALIAS).convert('1')
    draw.bitmap((40, 10), expression, fill=1)
    disp.image(image)
    disp.display()


class Camera(object):
    """Camera abstract class.
    By default this camera uses the openCV functionality.
    It can be inherited to overwrite methods in case another camera API exists.
    """

    def __init__(self, device_id=0, name='Camera'):
        # TODO load parameters from camera name. Use ``load`` method.
        self.device_id = device_id
        self.camera = None
        self.intrinsics = None
        self.distortion = None

    @property
    def intrinsics(self):
        return self._intrinsics

    @intrinsics.setter
    def intrinsics(self, intrinsics):
        self._intrinsics = intrinsics

    @property
    def distortion(self):
        return self._distortion

    @distortion.setter
    def distortion(self, distortion):
        self._distortion = distortion

    def start(self):
        """ Starts capturing device

        # Returns
            Camera object.
        """
        self.camera = cv2.VideoCapture(self.device_id)
        if self.camera is None or not self.camera.isOpened():
            raise ValueError('Unable to open device', self.device_id)
        return self.camera

    def stop(self):
        """ Stops capturing device.
        """
        return self.camera.release()

    def read(self):
        """Reads camera input and returns a frame.

        # Returns
            Image array.
        """
        frame = self.camera.read()[1]
        return frame

    def is_open(self):
        """Checks if camera is open.

        # Returns
            Boolean
        """
        return self.camera.isOpened()

    def calibrate(self):
        raise NotImplementedError

    def save(self, filepath):
        raise NotImplementedError

    def load(self, filepath):
        raise NotImplementedError


class VideoPlayer(object):
    """Performs visualization inferences in a real-time video.

    # Properties
        image_size: List of two integers. Output size of the displayed image.
        pipeline: Function. Should take RGB image as input and it should
            output a dictionary with key 'image' containing a visualization
            of the inferences. Built-in pipelines can be found in
            ``paz/processing/pipelines``.

    # Methods
        run()
        record()
    """

    def __init__(self, image_size, pipeline, camera):
        self.image_size = image_size
        self.pipeline = pipeline
        self.camera = camera

    def step(self):
        """ Runs the pipeline process once

        # Returns
            Inferences from ``pipeline``.
        """
        if self.camera.is_open() is False:
            raise ValueError('Camera has not started. Call ``start`` method.')

        frame = self.camera.read()
        if frame is None:
            print('Frame: None')
            return None
        # all pipelines start with an RGB image
        frame = convert_color_space(frame, BGR2RGB)
        return self.pipeline(frame)

    def run(self):
        """Opens camera and starts continuous inference using ``pipeline``,
        until the user presses ``q`` inside the opened window.
        """
        self.camera.start()
        global recordNum
        recordNum = tts()
        mythread = Thread(target=playCalendar)
        mythread.setDaemon(True)
        mythread.start()
        while True:
            output = self.step()
            label = output['boxes2D']
#             print(readyToPlay)
            if len(label):
                label = label[0]
                emotion = label.class_name
                value = label.score
                print(emotion, value)
                expression(emotion)
            image = resize_image(output['image'], tuple(self.image_size))
            show_image(image, 'inference', wait=False)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.camera.stop()
        cv2.destroyAllWindows()

    def record(self, name='video.avi', fps=20, fourCC='XVID'):
        """Opens camera and records continuous inference using ``pipeline``.

        # Arguments
            name: String. Video name. Must include the postfix .avi.
            fps: Int. Frames per second.
            fourCC: String. Indicates the four character code of the video.
            e.g. XVID, MJPG, X264.
        """
        self.start()
        fourCC = cv2.VideoWriter_fourcc(*fourCC)
        writer = cv2.VideoWriter(name, fourCC, fps, self.image_size)
        while True:
            output = self.step()
            image = resize_image(output['image'], tuple(self.image_size))
            show_image(image, 'inference', wait=False)
            writer.write(image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.stop()
        writer.release()
        cv2.destroyAllWindows()
