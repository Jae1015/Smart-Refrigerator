from light import Luxmeter
import time
import requests
import RPi.GPIO as GPIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

url = "https://www.fast2sms.com/dev/bulk"
 
payload = "sender_id=FSTSMS&message=Your fridge is open&language=english&route=p&numbers=8076831842"
headers = {
 'authorization': "5EodL3zQ2gqhpWjs0GeyMi8YulntPRJfAKF6wTUabNHmSB47r1n0hpGLxyqzPZeBwWjTIUsJ275tivHg",
 'Content-Type': "application/x-www-form-urlencoded",
 'Cache-Control': "no-cache",
 }
buzzer=25
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,GPIO.LOW)
fromaddr = "nikitahillwoods@gmail.com"
toaddr = "jaspreet.k.c1996@gmail.com"
  
# instance of MIMEMultipart
msg = MIMEMultipart()
 
# storing the senders email address  
msg['From'] = fromaddr
 
# storing the receivers email address 
msg['To'] = toaddr
 
# storing the subject 
msg['Subject'] = "Urgent"
 
# string to store the body of the mail
body = "Your fridge is left open"
 
# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))
#class fo:
while True:
                tsl = Luxmeter()
                x=tsl.getLux(1)
                time.sleep(1)
                print "x",x
                if (x>20):
                        time.sleep(5)
                        x=tsl.getLux(1)
                        print "IN if, x",x
                        if (x>20):
                            GPIO.output(buzzer,GPIO.HIGH)
                            time.sleep(3)
                            response = requests.request("POST", url, data=payload, headers=headers)
                            print(response.text)
                            GPIO.output(buzzer,GPIO.LOW)
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

                            

#files=["1cam.jpg","2cam.jpg"]
"""for f in files:
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
    msg.attach(p)"""
 

                        
