from qrtools.qrtools import QR
import json
def decode_code(filepath):
    code = QR(filename=filepath)
    if code.decode():
        data = code.data
        data = str(data)
        print(data)
        k = json.loads(data)
        print(k)
    else:
        return False

if __name__ == "__main__":
    i = input()
    decode_code(i)

