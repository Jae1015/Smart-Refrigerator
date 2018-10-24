#!/usr/bin/env python
import urllib2,json
READ_API_KEY='M30VXOSFE462K5S2'
CHANNEL_ID='540395'
#def main():
conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"  % (CHANNEL_ID,READ_API_KEY))
response = conn.read()
print "http status code=%s" % (conn.getcode())
data=json.loads(response)
print data['field2'],data['created_at']
x=data['field2']
print x
z= x.encode('ascii','ignore')
print "z",type(z)
y=z.split(",")
print y
print type(y)
y=[element.capitalize() for element in y]
#for(i=0;i<y.length;i++):
    #y1=y[i].capitalize()
    #check.append(str(y1))

items1=["apple","mango"]
shop_list=[]

for i in y:
                        if i not in items1:
                                print "no match"
                                shop_list.append(i)
                        else:
                                continue
                        print "shopping list"
                        print shop_list


conn.close()
#if __name__ == '__main__':
#    main()
