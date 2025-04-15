import UTF8, sys

#encoder

#get bytes of string
str_bytes:bytes = bytes(sys.argv[1],'utf-8')

#encode bytes of string
en_bytes:bytes = UTF8.enSten(str_bytes)

#print bytes of encoded string as string
print(en_bytes.decode('utf-8'))
