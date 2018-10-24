# this script captures image with Pi Camera
# performs image recognition using AWS Rekognition Engine
# and then calls AWS Polly Speech Synthesis API to describe the items found in the image
import picamera
import serial
import time
import RPi.GPIO as gpio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# image recognition code
# takes an image file as input and
# returns the list of items recognized in the image
def image_recognition(image_file):

	# import aws boto3 library
	import boto3

	items = []

	# list of labels to be ignored as stop-words
	# mostly generic words like fruit, vegetable, food etc.
	stoplist = ['Fruit', 'Produce', 'Plant', 'Vegetable', 'Food','Flora','Nut','Leaf','Citrus Fruit','Grapefruit','Chair','Table','Furniture','Photo Booth','Toy','Pepper']

	# calling aws rekognition api on image-file
	client = boto3.client('rekognition',region_name='us-east-2')
	with open(image_file, "rb") as image:
		# object recognition from the image
		print "opened"
		result = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=20, MinConfidence=50)
		print "1"
		# processing json output to get image labels
		for label in result['Labels']:
			if label['Name'] not in stoplist:
				items.append(label['Name'])
				print "2"

	return items


#Bluetooth module
#port=serial.Serial("/dev/ttyS0",9600,timeout=3.0)
#print 'Bluetooth Communication Between RPI & Android mobile device'
#print 'Send something from Android device'

camera = picamera.PiCamera()

#while True:
 #   port.flushInput()
  #  port.flushOutput()
   # time.sleep(2)
    #rcv=port.read(50)
    #if (rcv=='1'):
     #   print 'received string from Android: '+rcv
      #  time.sleep(2)
        #keyin=raw_input('enter string to send: ')
        #port.write(keyin)
        #print 'send something from Android device'
i=1
s='cam.jpg'

while i<2:
    camera.start_preview()
    camera.capture(str(i)+s)
    i=i+1
    print "1"
    time.sleep(2)
                
camera.close()

# capture image and identify objects in the image
image_file = "1cam.jpg"
#capture_image(image_file)
print "function called"
items = image_recognition(image_file)
print "function returned"
print items

fromaddr = "nikitahillwoods@gmail.com"
toaddr = "joshi.nikita1396@gmail.com"
  
# instance of MIMEMultipart
msg = MIMEMultipart()
 
# storing the senders email address  
msg['From'] = fromaddr
 
# storing the receivers email address 
msg['To'] = toaddr
 
# storing the subject 
msg['Subject'] = "Subject of the Mail"
 
# string to store the body of the mail
body = str(items)
 
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

files=["1cam.jpg","2cam.jpg"]
for f in files:
    # open the file to be sent 
    filename = f
    attachment = open(f, "rb")
 
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
 
    # To change the payload into encoded form
    p.set_payload((attachment).read())
 
    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
 
# creates SMTP session
s1 = smtplib.SMTP('smtp.gmail.com', 587)
 
# start TLS for security
s1.starttls()
 
# Authentication
s1.login(fromaddr, "deepjoshi1231")
 
# Converts the Multipart msg into a string
text = msg.as_string()
print "before mail"
 
# sending the mail
s1.sendmail(fromaddr, toaddr, text)
print "mail sent"
 
# terminating the session
s1.quit()

