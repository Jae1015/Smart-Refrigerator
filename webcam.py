import cv2

camera = cv2.VideoCapture(0)
i = 0
while i < 1:
    raw_input('Press Enter to capture')
    return_value, image = camera.read()
    image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', image)
    cv2.imwrite('opencv'+str(i)+'.png', image)
    i=i+1
del(camera)
