import pyqrcode


def create(filename = "Test.png", data = "", error="H", scale = 5):
    Code = pyqrcode.create(data,error)
    Code.png(filename + ".png", scale)
    return True

data = "pm,id:123123,pc:XASD2,qty:123"
create(filename="H", data=str(data))

f = ["L", "M", "Q", "H"]

for x in range(4):
    data = "pm,id:"+ str(x) +",pc:XASD2,qty:123"
    create(filename=str(x),data=str(data),error=f[x])