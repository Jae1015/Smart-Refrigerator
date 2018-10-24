items1=['Apple','Mango','Plum']
items2=['Tomato','Apple']
items=items1+items2
print items
check=['Apple','Pear']
shop_list=[]
for i in check:
                        if i in items:
                                print "match",i
                                continue
                        else:
                                print "no match",i
                                shop_list.append(i)
print "shopping list"
print shop_list
