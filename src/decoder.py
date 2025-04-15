import UTF8, sys

#get array of codepoints of characters in encoded string
codp:list = UTF8.UTF8_den(sys.argv[1])

#get data from codepoints
datB:bytes = UTF8.deSten(codp)

#print decoded bytes as string
print(datB.decode('utf-8'))
