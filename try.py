f=open("entryid",'r')
y=f.read()
print (y)
f.close()
z=20
f=open("entryid",'w')
f.write(str(z))
f.close()

