import pyqrcode


def create(filename = "Test.png", data = "", error='H', scale = 6):
    Code = pyqrcode.create(data,error)
    Code.png(filename, scale)
    return True

data = {"PENNINEMANUFACTURING":{"ProductCode":"XASD2", "Quantity":"123"}}
create(filename="Test1", data=data)