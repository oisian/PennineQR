import time
import json
from PIL import Image
import zbarlight


def decode_code(filepath):
    file_path = filepath
    image = Image.open(file_path)
    image.load()
    start = time.time()
    codes = zbarlight.scan_codes('qrcode', image)
    end = time.time()
    print(end - start)

    json.o
    print('QR codes: %s' % codes)




if __name__ == "__main__":
    i = input()
    decode_code(i)

