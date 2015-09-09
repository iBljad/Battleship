mess = open("C:\Intel\mess.txt", 'r')
text = mess.read()
result = ''
for i in text:
    if ord('z') >= ord(i) >= ord('a'):
        result += i
    """elif i == 'y':
        result += 'a'
    elif i == 'z':
        result += 'b'
    else:
        result += i"""
print(result)
