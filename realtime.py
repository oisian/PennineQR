import cv2

title = "Dynamsoft Barcode Reader"
cv2.namedWindow(title, 1)
capture = cv2.VideoCapture(0)

while True:
    result, img = capture.read()
    cv2.imshow(title, img)