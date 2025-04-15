OCTPR  = 0b10000000
PB2    = 0b11000000
PB3    = 0b11100000
PB4    = 0b11110000
MASK3  = 0b00000111
MASK4  = 0b00001111
MASK5  = 0b00011111
MASK6  = 0b00111111
MASK8  = 0b11111111
RMASK2 = 0b11000000
RMASK3 = 0b11100000
RMASK4 = 0b11110000
RMASK5 = 0b11111000


#function to calculate amount of encoded data will take in bytes

def getEnLen(length:int) -> int:
  res=0
  res=(length//3)*6
  res+=(length%3)*3
  return res

#function to calculate amount of decoded data will take in bytes

def getStenLen(arr:list) -> int:
  length=len(arr)
  res=0
  bits=0

  for el in arr :
    if (el<=0x8fff and el>=0x8000):
      bits+=12

    elif (el<=0xff):
      bits+=8

    res+=bits//8
    bits=bits%8

  if (bits>0):
    res+=1

  return res

#functions to get value of specific bit in number

def gBit(num:int, ind:int) -> int:
  return (num>>ind)&1

#function to encode single code point into UTF-8
#it recives unsigned code and returns structure of array of bytes

def UTF8_enc(code:int) -> bytes:
  byte_res:bytes = bytes(chr(code),'UTF-8')
  
  return byte_res

#function to calculate length of string not by bytes but by characters, including UTF-8 characters

def calcLen(string:str) -> int:
  res:int = len(string)
  return res

#function to deencode string that contains UTF-8 characters and returns structure with array of codepoints of characters

def UTF8_den( byte_s:str ) -> list:
  
  res:list=[]
  for ch in byte_s:
    res.append(ord(ch))

  return res

#function to encode bytes in UTF-8 characters
#recives bytes, and returns bytes of string with data stored in UTF-8 characters

def enSten(arr:bytes) -> str:
  length=len(arr)
  enLen=getEnLen(length)
  res:bytes=b''

  codePoint=0x8000
  subB=0
  bits=0
  cary=0
  shift=0
  bitsPass=0
  dataI=0
  i=0

  while(i < length):
    if(bits<=0):
      bits=8
    
    cary=12-subB
    shift=subB


    if (bits<=cary):
      subB+=bits
      codePoint|=((arr[i]>>bitsPass)&((1<<bits)-1))<<shift
      bits=0
      bitsPass=0
      i+=1

    elif (bits>cary):
      subB=12
      codePoint|=((arr[i]>>bitsPass)&((1<<cary)-1))<<shift
      bits-=cary
      bitsPass=cary


    if (subB>=12 or (i>=length)):
      utf:bytes = UTF8_enc(codePoint)
      res+=utf
      dataI+=len(utf)
      codePoint=0x8000
    

    subB%=12
  

  return res

#function to decode data from array of codepoints
#decodes result of enSten function

#recives array of codepoints of characters in encoded string
#returns bytes of decoded string

def deSten(arr:list) -> bytes:
  length=len(arr)
  i_res=[0]*getStenLen(arr)

  dataI=0
  bits=0
  bitsPass=0
  subB=0
  cary=0
  shift=0
  proc=False


  for i in range(length):
    proc=False
    bitsPass=0
    bits=0

    if (arr[i]<=0x8fff and arr[i]>=0x8000):
      bits=12
      proc=True

    elif (arr[i]<=0x8ff and arr[i]>=0x800):
      bits=8
      proc=True
      
    elif (arr[i]<=0xff):
      bits=8
      proc=True
    
    
    #proccess data
    while(bits>0 and proc):
      cary=8-subB
      shift=subB

      if(bits<=cary):
        subB+=bits
        i_res[dataI] |= (((arr[i]>>bitsPass)&((1<<bits)-1))<<shift)&0xff
        bits=0

      elif (bits>cary):
        subB=8
        i_res[dataI] |= (((arr[i]>>bitsPass)&((1<<cary)-1))<<shift)&0xff
        bits-=cary
        bitsPass+=cary
        
      dataI+=subB//8
      subB%=8


  return bytes(i_res)



