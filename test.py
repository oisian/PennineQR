import cv2, time
FPS = 0
cap = cv2.VideoCapture(0)

last = time.time()

for i in range(0,100):
    before = time.time()
    rval, frame = cap.read()
    now = time.time()
    print("cap.read() took: " + str(now - before))
    if(now - last >= 1):
        print(FPS)
        last = now
        FPS = 0
    else:
        FPS += 1
cap.release()