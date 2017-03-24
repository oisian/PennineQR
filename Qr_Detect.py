import cv2
import numpy as np
from threading import Thread
import subprocess
import queue


class CodeDetection():
    def __init__(self):
        self.stopped = False
        self.frame = queue.Queue()
        self.QRBoundingBox = None
        self.detect_mode = "Zbar"
        self.data = None

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.detect).start()
        return self

    def detect(self):
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                return

            if self.frame.qsize() > 50:
                while not self.frame.empty():
                    self.frame.get()

            if not self.frame.empty():

                # if the thread indicator variable is set, stop the thread
                # cv2.imshow("preview", self.frame)
                frame = self.frame.get()
                gray = frame

                # compute the Scharr gradient magnitude representation of the images
                # in both the x and y direction
                gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
                gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

                # subtract the y-gradient from the x-gradient
                gradient = cv2.subtract(gradX, gradY)
                gradient = cv2.convertScaleAbs(gradient)

                # blur and threshold the image
                blurred = cv2.blur(gradient, (9, 9))
                (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

                # construct a closing kernel and apply it to the thresholded image
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 17))
                closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

                # perform a series of erosions and dilations
                closed = cv2.erode(closed, None, iterations=10)
                closed = cv2.dilate(closed, None, iterations=10)

                # find the contours in the thresholded image
                _, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # if no contours were found, return None
                if len(cnts) != 0:
                    # otherwise, sort the contours by area and compute the rotated
                    # bounding box of the largest contour
                    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                    x, y, width, height = cv2.boundingRect(c)

                    if (x - 30 > 0):
                        x = x - 20
                    else:
                        x = 0

                    if (y - 30 > 0):
                        y = y - 20
                    else:
                        y = 0

                    roi = frame[y:y + height + 40, x:x + width + 40]
                    dst = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
                    self.decodeQr(dst)
                else:
                    self.QRBoundingBox = None

    def decodeQr(self, img):
        if img != None:
            blur = cv2.GaussianBlur(img, (5, 5), 0)
            ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite("roi.png", th3)
            if self.detect_mode == "Zxing":
                self.data = self.zxing_detect()
            if self.detect_mode == "Zbar":
                cmd = ['C:/Python27/zbarimg.exe', '-q', 'C:/Users/jkirkpatrick/Desktop/PennineQR/roi.png']
                (stdout, stderr) = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                                    universal_newlines=True).communicate()
                self.data = stdout
                while not self.frame.empty():
                    self.frame.get()

    def giveFrame(self, frame):
        self.frame.put(frame)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
