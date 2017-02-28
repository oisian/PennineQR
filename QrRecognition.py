import cv2
import numpy as np
import QRCodeDetection as QR
#import zxing
import time
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

qrDetector = QR.QrCodeDetection()

while rval:

    result = qrDetector.detect(frame)

    if (result != None):
        cv2.imwrite("roi.png", result)

        cv2.imshow("preview", result)
        #reader = zxing.BarCodeReader("C:/zxing-master")

        #barcode = reader.decode("roi.png")

        #if barcode != None:
        #    print(barcode.data)


    cv2.imshow("pre", frame)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
