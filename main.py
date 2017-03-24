import cv2
try:
    import zbarlight
except ImportError:
    pass
try:
    import zxing
except ImportError:
    pass
import Stream
from connect import main
import Qr_Detect
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
        self.detect_mode = "Zbar";
        self.last_code = None

    def start(self):
        self.poster = main.connection().start()
        self.stream = Stream.WebcamVideoStream(src=0).start()
        self.detector = Qr_Detect.CodeDetection().start() #Qr_Detect.CodeDetection().start()
        self.ip = self.poster.ip
        Thread(target=self.loop, args=()).start()
        return self

    def loop(self):
        while True:
            if self.stopped:
                self.close_program()
                return

            frame = self.stream.read()
            self.detector.frame.put(frame)

            if self.detector.QRBoundingBox !=  None:
                cv2.drawContours(frame, [self.detector.QRBoundingBox], 0, (0, 0, 255), 2)

            cv2.imshow("Window", frame)

            if self.detector.data:
                self.parse_send_data(self.detector.data)

            if self.show_image:
                key = cv2.waitKey(20)
                if key == 27:  # exit on ESC
                    break

    def zxing_detect(self):
        reader = zxing.BarCodeReader("C:/zxing/")
        barcode = reader.decode("roi.png")
        return barcode

    def parse_send_data(self, barcode):
        if barcode != None:
            if self.detect_mode == "Zxing":
                data = barcode.data
                splitData = data.split(",")
                if splitData[0] == "pm":
                    UNID = splitData[1].split(":")[1].rstrip()
                    productCode = splitData[2].split(":")[1].rstrip()
                    Quantity = splitData[3].split(":")[1].rstrip()
                    if productCode and Quantity:
                        if self.last_code != UNID:
                            self.poster.requests.append(
                                {"IP": self.ip, "UNID": UNID, 'ProductCode': productCode, 'Quantity': Quantity})
                            self.last_code = UNID;

            else:
                data = barcode
                splitData = data.split(",")
                if splitData[0] == "QR-Code:pm":
                    UNID = splitData[1].split(":")[1].rstrip()
                    productCode = splitData[2].split(":")[1].rstrip()
                    Quantity = splitData[3].split(":")[1].rstrip()
                    if productCode and Quantity:
                        if self.last_code != UNID:
                            self.poster.requests.append(
                                {"IP": self.ip, "UNID": UNID, 'ProductCode': productCode, 'Quantity': Quantity})
                            self.last_code = UNID;

    def hold_check(self):
        pass

    def close_program(self):
        cv2.destroyAllWindows()
        self.stream.stop()
        self.detector.stop()
        self.poster.stop()



sm = StockMovement(show_image=True).start()
