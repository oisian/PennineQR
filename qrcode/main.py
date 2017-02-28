from Stream import WebcamVideoStream
from realtime import CodeDetection

import cv2

vs = WebcamVideoStream(src=0).start()
detection = CodeDetection()
detection.start()

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    # check to see if the frame should be displayed to our screen
    img = detection.detect(frame)
    if img != None:
        cv2.imshow("Frame", img)
        cv2.imwrite("roi.png", img)

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break



# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
detection.stop()