from qrcode import Stream
from qrcode import realtime
from connect import main
import zxing
import json
import zbarlight

import cv2

con = main.connection()
con.start()

vs = Stream.WebcamVideoStream(src=0).start()
detection = realtime.CodeDetection()
detection.start()


ip = con.ip
ip1 = ip
ip2 = '192.168.0.56'

while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels

    frame = vs.read()
    cv2.imshow("ee", frame)
    # check to see if the frame should be displayed to our screen
    img = detection.detect(frame)
    if img != None:
        cv2.imshow("Frame", img)
        cv2.imwrite("roi.png", img)
        reader = zxing.BarCodeReader("C:/zxing/")
        barcode = reader.decode("C:/Users/jkirkpatrick/Desktop/PennineQR/roi.png",try_harder=True)
        print(barcode)
        if barcode != None:
            data = barcode.data
            splitData = data.split(",")
            if splitData[0] == "PM":
                print(splitData)
                UNID = splitData[1].split(":")[1].rstrip()
                productCode = splitData[2].split(":")[1].rstrip()
                Quantity = splitData[3].split(":")[1].rstrip()
                if productCode and Quantity:
                    con.requests.append({"IP": ip,"UNID": UNID, 'ProductCode': productCode, 'Quantity': Quantity})
                    if ip == ip1:
                        ip = ip2
                    else:
                        ip = ip1
        else:
            print("no code")

    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
detection.stop()
