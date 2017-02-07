from qrtools import QR
import json
def decode_code(filepath):
    code = QR(filename=filepath)
    if code.decode():
        data = code.data_to_string()
        json = json.loads(data)
        print data
        print json
    else:
        return False

if __name__ == "__main__":
    i = raw_input()
    decode_code(i)

