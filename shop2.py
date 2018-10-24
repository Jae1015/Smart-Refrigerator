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
import urllib2
import json
import cv2
from PIL import Image

READ_API_KEY='M30VXOSFE462K5S2'
CHANNEL_ID='540395'
check=[]
shop_list=[]
items1= []
items2= []
# image recognition code
# takes an image file as input and
# returns the list of items recognized in the image
def image_recognition(image_file):

	# import aws boto3 library
	import boto3

	items = []

	# list of labels to be ignored as stop-words
	# mostly generic words like fruit, vegetable, food etc.
	stoplist = ['Bell Pepper','Quince','Papaya','Bowl','Banana','Squash','Persimmon','Vase','Potted Plant','Egg','Dish','Meal','Beverage','Drink','Juice','Plate','Jar','Cherry','Carrot','Peach','Pottery','Fruit', 'Produce', 'Plant', 'Vegetable', 'Food','Flora','Nut','Leaf','Citrus Fruit','Grapefruit','Chair','Table','Furniture','Photo Booth','Toy','Pepper']

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

#class list_formation:
while True:
                conn = urllib2.urlopen("https://api.thingspeak.com/channels/540395/feeds.json?api_key=M30VXOSFE462K5S2&results=1")
                response = conn.read()
                print "http status code=%s" % (conn.getcode())
                print "conn established"
                data=json.loads(response)
                print "no input"
                time.sleep(3)
                #data['feeds'][0]['field1']

                f=open("entryid",'r')
                y=f.read()
                print "y",y
                f.close()

                z=(data['feeds'][0]['entry_id'])
                print "z",z

                if(int(y)!=z):
                        f=open("entryid",'w')
                        f.write(str(z))
                        f.close()
                        print "got an input"
                        camera = picamera.PiCamera()
                        

                        s='cam.jpg'
                        i=1

                        camera.start_preview()
                        camera.capture(str(i)+s)
                        i=i+1
                        print "1"
                        time.sleep(2)
                
                        camera.close()

                        cap = cv2.VideoCapture(0)

                        j = 0
                        while j < 1:
                            #raw_input('Press Enter to capture')
                            return_value, image = cap.read()
                            image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                            cv2.imshow('Input', image)
                            cv2.imwrite(str(i)+s, image)
                            j=+1
                        del(cap)

                        #resolution
                        size=640,480
                        im=Image.open("1cam.jpg")
                        resized=im.resize(size,Image.ANTIALIAS)
                        resized.save("1cam.jpg")

                        im1=Image.open("2cam.jpg")
                        resized=im1.resize(size,Image.ANTIALIAS)
                        resized.save("2cam.jpg")
                
                # capture image and identify objects in the image
                        image_file1 = "1cam.jpg"
                        image_file2 = "2cam.jpg"

       
                
               

                #capture_image(image_file)
                        print "function called"
                        items1 = image_recognition(image_file1)
                        items2 = image_recognition(image_file2)
                        print "function returned"
                        print "detected1",items1
                        print "detected2",items2

                        items=items1+items2
                        #items from use
                        print "items",items
                        conn1 = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"  % (CHANNEL_ID,READ_API_KEY))
                        response = conn.read()
                        print "http status code=%s" % (conn.getcode())
                        #data=json.loads(response)
                        #print data['field2'],data['created_at']
                        x=data['feeds'][0]['field2']
                        print x
                        z= x.encode('ascii','ignore')
                        #print "z",type(z)
                        y=z.split(",")
                        print y
                        conn1.close()
                        check=[element.capitalize() for element in y]
                        print "check",check

                        for i in check:
                                if i in items:
                                        print "match",i
                                        continue
                                else:
                                        print "no match",i
                                        shop_list.append(i)
                        print "shopping list"
                        print shop_list
                
                        fromaddr = "nikitahillwoods@gmail.com"
                        toaddr = "joshi.nikita1396@gmail.com"
  
                        # instance of MIMEMultipart
                        msg = MIMEMultipart()
 
                        # storing the senders email address  
                        msg['From'] = fromaddr
 
                        # storing the receivers email address 
                        msg['To'] = toaddr
 
                        # storing the subject 
                        msg['Subject'] = "Your Shopping list"
 
                        # string to store the body of the mail
                        body = str(shop_list)
         
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
                        shop_list=[]
conn.close()

