import cv2
# import zxing
import zbarlight
from  PIL import Image
import Stream
from connect import main
import realtime
import time
from threading import Thread


class StockMovement:
    def __init__(self, show_image=False):
        # flag to brake out of the main loop
        self.stopped = False
        # Class in charge of sending data to web server
        self.poster = None;
        # Class in charge of detecting if possiable QR code in frame
        self.detector = None;
        # Class in charge of getting Cam stream
        self.stream = None
        # flag to determain if stream should be shown
        self.show_image = show_image
        # current frame from camera
        self.frame = None

        # Ip address of terminal
        self.ip = None
        self.ip1 = '192.168.0.56'
        # flag to wait for QR to pass
        self.hold = False

        self.detect_mode = "Zbar";

    def start(self):
        self.poster = main.connection().start()
        self.stream = Stream.WebcamVideoStream(src=0).start()
        self.detector = realtime.CodeDetection().start()
        self.ip = self.poster.ip
        Thread(target=self.loop, args=()).start()
        return self

    def loop(self):
        while True:
            if self.stopped:
                self.close_program()
                return

            self.frame = self.stream.read()
            if self.show_image:
                cv2.imshow("Unprocessed Frame", self.frame)
            if not self.hold:
                img = self.detector.detect(self.frame)
                if img != None:
                    if self.show_image:
                        cv2.imshow("Frame", img)
                    cv2.imwrite("roi.png", img)
                    if self.detect_mode == "Zxing":
                        self.xzing_detext(img)
                        self.hold = False

                    if self.detect_mode == "Zbar":
                        self.zbar_detext(img)
                        self.hold = False
            else:
                self.hold_check()

            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break

    def zbar_detect(self):
        file_path = 'roi.png'
        with open(file_path, 'rb') as image_file:
            image = Image.open(image_file)
            image.load()

        codes = zbarlight.scan_codes('qrcode', image)
        print('QR codes: %s' % codes)
        return codes

    def zxing_detext(self, img):
        cv2.imwrite("roi.png", img)
        reader = zxing.BarCodeReader("C:/zxing/")
        barcode = reader.decode("roi.png")
        if barcode != None:
            data = barcode.data
            splitData = data.split(",")
            if splitData[0] == "pm":
                UNID = splitData[1].split(":")[1].rstrip()
                productCode = splitData[2].split(":")[1].rstrip()
                Quantity = splitData[3].split(":")[1].rstrip()
                if productCode and Quantity:
                    self.poster.requests.append(
                        {"IP": self.ip, "UNID": UNID, 'ProductCode': productCode, 'Quantity': Quantity})
                    if self.ip == self.ip1:
                        self.ip = self.poster.ip
                    else:
                        self.ip = self.ip1

    def hold_check(self):
        pass

    def close_program(self):
        cv2.destroyAllWindows()
        self.stream.stop()
        self.detector.stop()
        self.poster.stop()


sm = StockMovement(show_image=False).start()
