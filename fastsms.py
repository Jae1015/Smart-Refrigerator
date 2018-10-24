import requests
 
url = "https://www.fast2sms.com/dev/bulk"
 
payload = "sender_id=FSTSMS&message=fridge open&language=english&route=p&numbers=8178257399,9711854779"
headers = {
 'authorization': "jx4B2DBhUSgHsaQnJ0Gtbudjyy2cTxqdpEWpX4eWztNe13H01OaBfb3TjCS9",
 'Content-Type': "application/x-www-form-urlencoded",
 'Cache-Control': "no-cache",
 }
 
response = requests.request("POST", url, data=payload, headers=headers)
 
print(response.text)
