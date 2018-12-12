import re

import math as MH

content = r'<?xml version="1.0" encoding="GB2312"?>'
charset = re.compile(".*\s*encoding=\"([^\"]+)\".*", re.M).match(content)

print(charset.group(0))
print(charset.group(1))
# m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
 
# print ("m.string:", m.string)
# print ("m.re:", m.re)
# print ("m.pos:", m.pos)
# print ("m.endpos:", m.endpos)
# print ("m.lastindex:", m.lastindex)
# print ("m.lastgroup:", m.lastgroup)

# print ("m.group(1,2):", m.group(1, 2))
# print ("m.groups():", m.groups())
# print ("m.groupdict():", m.groupdict())
# print ("m.start(2):", m.start(2))
# print ("m.end(2):", m.end(2))
# print ("m.span(2):", m.span(2))
# print (r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3'))

# p = re.compile(r'(i)(\s)')
# s = 'i say, hello world!'

# ma = p.match(s)
# print(ma)

# se = p.search(s)
# print(se)

# fial = p.findall(s)
# print(fial)

# print (p.sub(r'\2 \1', s))

# day = "2017-01-22"

# print(re.sub(\
# "(\d{4})-(\d{2})-(\d{2})",r"\2/\3/\1",day))

# print(re.sub(\
# "(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})",\
# "\g<month>/\g<day>/\g<year>",day))

# lis = range(100)

# for i in lis :
#     print(i)
# print(lis)

# print(MH.pi)
# print(MH.e)

# list1 = [1]
# print(list1)

# tup1 = 1,
# print(tup1)

# map = {'one':1, 1:'one',(1,2):[1,2,3,4,5]}
# lis = map.items()
# print(type(lis))
# print(lis)
# print(map)
# for key,values in map.items():
#     print(key, values)

# str = "hellow world"

# print(str[1])

# print(str)

# #可写函数说明
# def printinfo(name, age = 35):
#     "打印任何传入的字符串"
#     print("Name:%s age %u", name, age);
#     print("Age:", age);
#     return;
 
# #调用printinfo函数
# printinfo("miki");
# printinfo( name="miki" );