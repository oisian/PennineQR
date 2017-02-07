import pyqrcode


def create(filename = "Test.png", data = "", error='H', scale = 6):
    Code = pyqrcode.create(data,error)
    Code.png(filename, scale)
    return True