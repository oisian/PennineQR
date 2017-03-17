import cv2
import numpy as np
from threading import Thread
#import zxing
import time
import cProfile

class CodeDetection():
    def __init__(self):
        self.stopped = False
        self.frame = None

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.detect)
        return self

    def detect(self, frame):
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                return

            if frame != None:
                self.frame = frame
            # if the thread indicator variable is set, stop the thread
                #cv2.imshow("preview", self.frame)
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

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
                closed = cv2.erode(closed, None, iterations=25)
                closed = cv2.dilate(closed, None, iterations=25)

                # find the contours in the thresholded image
                _, cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # if no contours were found, return None
                if len(cnts) == 0:
                    return None

                # otherwise, sort the contours by area and compute the rotated
                # bounding box of the largest contour
                c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

                # Draw box on screen


                x, y, width, height = cv2.boundingRect(c)
                if (x - 30 > 0):
                    x = x - 30
                else:
                    x = 0

                if (y - 30 > 0):
                    y = y - 30
                else:
                    y = 0
                roi = frame[y:y + height + 60, x:x + width + 60]
                dst = cv2.resize(roi, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

                #rect = cv2.minAreaRect(c)
                #box = cv2.boxPoints(rect)
                #box = np.int0(box)
                #cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                #cv2.imshow("dd", frame)
                return dst


    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
