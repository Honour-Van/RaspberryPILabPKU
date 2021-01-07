import argparse
from emo.backend.camera import VideoPlayer
from emo.backend.camera import Camera
from emo.pipelines import DetectMiniXceptionFER
from threading import Thread
from ptt import pressToTalk
import os
import sys

thread_ptt = Thread(target=pressToTalk, args=(4, ))
thread_ptt.setDaemon(True)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description='Real-time face classifier')
        parser.add_argument('-c', '--camera_id', type=int, default=0,
                            help='Camera device ID')
        parser.add_argument('-o', '--offset', type=float, default=0.1,
                            help='Scaled offset to be added to bounding boxes')
        args = parser.parse_args()

        pipeline = DetectMiniXceptionFER([args.offset, args.offset])
        camera = Camera(args.camera_id)
        player = VideoPlayer((640, 480), pipeline, camera)

        thread_ptt.start()
        player.run()
    except KeyboardInterrupt:
        pass
