from qrtools import QR

def decode_code(filepath):
    code = QR(filename=filepath)
    if code.decode():
        print code.data_to_string()
    else:
        return False

if __name__ == "__main__":
    i = input()
    print i
    decode_code(i)

