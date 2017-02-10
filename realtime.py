import cv2.cv as cv

title = "Dynamsoft Barcode Reader"
cv.NamedWindow(title, 1)
capture = cv.CaptureFromCAM(0)

while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage(title, img)