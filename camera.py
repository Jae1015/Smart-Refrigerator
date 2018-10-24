import picamera
import serial
import time
from PIL import Image
i=1
camera = picamera.PiCamera()
s='cam.jpg'
camera.start_preview()
camera.capture(str(i)+s)

print "1"
time.sleep(2)
size=640,480
im=Image.open("1cam.jpg")
resized=im.resize(size,Image.ANTIALIAS)
resized.save("1cam.jpg")

                
camera.close()
              
