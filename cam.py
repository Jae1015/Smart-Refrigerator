from PIL import Image
size=640,480
im=Image.open("icam.jpeg")
resized=im.resize(size,Image.ANTIALIAS)
resized.save("3cam.jpeg")
