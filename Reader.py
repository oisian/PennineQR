
import json
from PIL import Image
import zbarlight
def decode_code(filepath):
    file_path = filepath
    with open(file_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes('qrcode', image)
    print('QR codes: %s' % codes)

if __name__ == "__main__":
    i = input()
    decode_code(i)

