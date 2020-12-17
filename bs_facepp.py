# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import base64
import requests
from cv2 import cv2
from threading import Thread

# connect to online face++ API
BASE_URL = "https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton"
API_KEY = "unE76-N-53r2C0BDp7dBcQTJFiL5LJsp"
API_SECRET = "pGEsqdOXJTy_Ml9KQZc5XiWqxps3oVRK"
data = {"api_key": API_KEY, "api_secret": API_SECRET}


class VideoStreamWidget(object):
    def __init__(self, src=1):
        self.capture = cv2.VideoCapture(src)
        # Change the image resolution
        self.capture.set(3, 640)
        self.capture.set(4, 480)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):

        # process the frame
        encoded_frame = frame_base64(self.status, self.frame)
        body = upload_body(encoded_frame)

        # check if there is any detected body
        if body is not None:
            if len(body) > 0:
                # when the body is detected
                for i in range(0, len(body)):
                    # gain a dict of each body location
                    body_location = body[i]['body_rectangle']
                    # gain a dict of each body landmarks
                    keypoint = body[i]['landmark']
                    # call function to draw lines
                    draw_line(keypoint, body_location, self.frame)
            else:
                pass
        else:
            pass

        # Display frames in main program
        cv2.imshow('Video', self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)


# * use base64 to encode a video frame
def frame_base64(retval, frame):
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text


# * upload the image to test
def upload_body(encoded_text):
    data.update({"image_base64": encoded_text})
    time6 = time.time()
    response = requests.post(url=BASE_URL, data=data)
    body = response.json().get('skeletons')
    time7 = time.time()
    print("The post time is: ", (time7 - time6))
    return body


# * draw lines to connect all detected landmark
def draw_line(keypoint, body_location, img):
    # gain the location of body
    t = body_location.get("top")
    l = body_location.get("left")
    h = body_location.get("height")
    w = body_location.get("width")
    # show the position rectangle of body
    cv2.rectangle(img, (l, t), (w + l, h + t), (0, 0, 255), 2)
    # draw lines connect body part
    # head ---> neck
    cv2.line(img, (int(keypoint['head']['x'] + l), int(keypoint['head']['y'] + t)),
             (int(keypoint['neck']['x'] + l), int(keypoint['neck']['y'] + t)), (0, 255, 0), 2)
    # neck --> left_shoulder
    cv2.line(img, (int(keypoint['neck']['x'] + l), int(keypoint['neck']['y'] + t)),
             (int(keypoint['left_shoulder']['x'] + l), int(keypoint['left_shoulder']['y'] + t)), (0, 255, 0), 2)
    # neck --> right_shoulder
    cv2.line(img, (int(keypoint['neck']['x'] + l), int(keypoint['neck']['y'] + t)),
             (int(keypoint['right_shoulder']['x'] + l), int(keypoint['right_shoulder']['y'] + t)), (0, 255, 0), 2)
    # left_shoulder --> left_elbow
    cv2.line(img, (int(keypoint['left_shoulder']['x'] + l), int(keypoint['left_shoulder']['y'] + t)),
             (int(keypoint['left_elbow']['x'] + l), int(keypoint['left_elbow']['y'] + t)), (0, 255, 0), 2)
    # left_elbow --> left_hand
    cv2.line(img, (int(keypoint['left_elbow']['x'] + l), int(keypoint['left_elbow']['y'] + t)),
             (int(keypoint['left_hand']['x'] + l), int(keypoint['left_hand']['y'] + t)), (0, 255, 0), 2)
    # right_shoulder --> right_elbow
    cv2.line(img, (int(keypoint['right_shoulder']['x'] + l), int(keypoint['right_shoulder']['y'] + t)),
             (int(keypoint['right_elbow']['x'] + l), int(keypoint['right_elbow']['y'] + t)), (0, 255, 0), 2)
    # right_elbow --> right_hand
    cv2.line(img, (int(keypoint['right_elbow']['x'] + l), int(keypoint['right_elbow']['y'] + t)),
             (int(keypoint['right_hand']['x'] + l), int(keypoint['right_hand']['y'] + t)), (0, 255, 0), 2)
    # neck --> left_buttocks
    cv2.line(img, (int(keypoint['neck']['x'] + l), int(keypoint['neck']['y'] + t)),
             (int(keypoint['left_buttocks']['x'] + l), int(keypoint['left_buttocks']['y'] + t)), (0, 255, 0), 2)
    # neck --> right_buttocks
    cv2.line(img, (int(keypoint['neck']['x'] + l), int(keypoint['neck']['y'] + t)),
             (int(keypoint['right_buttocks']['x'] + l), int(keypoint['right_buttocks']['y'] + t)), (0, 255, 0), 2)
    # left_buttocks --> left_knee
    cv2.line(img, (int(keypoint['left_buttocks']['x'] + l), int(keypoint['left_buttocks']['y'] + t)),
             (int(keypoint['left_knee']['x'] + l), int(keypoint['left_knee']['y'] + t)), (0, 255, 0), 2)
    # right_buttocks --> right_knee
    cv2.line(img, (int(keypoint['right_buttocks']['x'] + l), int(keypoint['right_buttocks']['y'] + t)),
             (int(keypoint['right_knee']['x'] + l), int(keypoint['right_knee']['y'] + t)), (0, 255, 0), 2)
    # left_buttocks --> right_buttocks
    cv2.line(img, (int(keypoint['left_buttocks']['x'] + l), int(keypoint['left_buttocks']['y'] + t)),
             (int(keypoint['right_buttocks']['x'] + l), int(keypoint['right_buttocks']['y'] + t)), (0, 255, 0), 2)
    # left_knee --> left_foot
    cv2.line(img, (int(keypoint['left_knee']['x'] + l), int(keypoint['left_knee']['y'] + t)),
             (int(keypoint['left_foot']['x'] + l), int(keypoint['left_foot']['y'] + t)), (0, 255, 0), 2)
    # right_knee --> right_foot
    cv2.line(img, (int(keypoint['right_knee']['x'] + l), int(keypoint['right_knee']['y'] + t)),
             (int(keypoint['right_foot']['x'] + l), int(keypoint['right_foot']['y'] + t)), (0, 255, 0), 2)


if __name__ == "__main__":
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass

