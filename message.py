import way2sms
username='9582454540'
password='deepajoshi'
q=way2sms.Sms(username,password)
q.send('9711854779','hallo')# both are STRING
print ("msg sent")
#q.msgSentToday()
q.logout()
