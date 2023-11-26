from Crypto.Cipher import Blowfish
from Crypto import Random
import secrets
import string
from PIL import Image


# KEY GENERATION,ENCODING,DECODING
def generate_random_key(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key

def pad(data):
    length = 8 - (len(data) % 8)
    return data + (chr(length) * length).encode()

def encrypt(data):
    key = bytes(generate_random_key(16),'utf-8')  # Generate a random key
    data = pad(data)
    iv = Random.new().read(Blowfish.block_size)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    return key, iv + cipher.encrypt(data)

def decrypt(key, data):
    iv = data[:Blowfish.block_size]
    data = data[Blowfish.block_size:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    padding_length = decrypted_data[-1]
    return decrypted_data[:-padding_length]


# REAL ENCRYPTION 


# Convert encoding data into 8-bit binary
def genData(data):

    newd = []

    for i in data:
      newd.append(format(ord(i), '08b'))
    return newd

# Pixels are modified according to the 8-bit binary data and finally returned
def modPix(pix, data):

  datalist = genData(data)
  lendata = len(datalist)
  imdata = iter(pix)

  for i in range(lendata):

    # Extracting 3 pixels at a time
    pix = [value for value in imdata.__next__()[:3] +
                imdata.__next__()[:3] +
                imdata.__next__()[:3]]
    
    for j in range(0, 8):
      if (datalist[i][j] == '0' and pix[j]% 2 != 0):
        pix[j] -= 1

      elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
        if(pix[j] != 0):
          pix[j] -= 1
        else:
          pix[j] += 1


    if (i == lendata - 1):
      if (pix[-1] % 2 == 0):
        if(pix[-1] != 0):
          pix[-1] -= 1
        else:
          pix[-1] += 1

    else:
      if (pix[-1] % 2 != 0):
        pix[-1] -= 1

    pix = tuple(pix)
    yield pix[0:3]
    yield pix[3:6]
    yield pix[6:9]


# for geting encoded pixels and embedding in new image1
def encode_enc(newimg, data):
  w = newimg.size[0]
  (x, y) = (0, 0)

  for pixel in modPix(newimg.getdata(), data):

    # Putting modified pixels in the new image
    newimg.putpixel((x, y), pixel)
    if (x == w - 1):
      x = 0
      y += 1
    else:
      x += 1

# Encode data into image
def encode():
  img = input("Enter image name(with extension) : ")
  image = Image.open(img, 'r')

  data = input("Enter data to be encoded : ")
  if (len(data) == 0):
    raise ValueError('Data is empty')

  newimg = image.copy()

  plaintext = bytes(data, 'utf-8')

  key, encrypted = encrypt(plaintext)
  

  print('Plaintext:', plaintext)
  print('Key:', key)
  print('Encrypted:', encrypted)
  
  print(str(encrypted)[2:-1])
  encode_enc(newimg, str(encrypted)[2:-1])

  new_img_name = input("Enter the name of new image(with extension) : ")
  newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
  img = input("Enter image name(with extension) : ")
  image = Image.open(img, 'r')


  data = ''
  imgdata = iter(image.getdata())

  while (True):
    pixels = [value for value in imgdata.__next__()[:3] +
                imgdata.__next__()[:3] +
                imgdata.__next__()[:3]]

    # string of binary data
    binstr = ''

    for i in pixels[:8]:
      if (i % 2 == 0):
        binstr += '0'
      else:
        binstr += '1'

    data += chr(int(binstr, 2))
    if (pixels[-1] % 2 != 0):
      key = input("Please input the key : ")
      key = bytes(key, 'utf-8')
      print(data)
      data = data.encode().decode('unicode_escape').encode("raw_unicode_escape")
      print(data)
      
      decrypted = decrypt(key, data)
      return str(decrypted)[2:-1]

# Main Function
def main():
  a = int(input(":: Welcome to Steganography ::\n"
            "1. Encode\n2. Decode\n"))
  if (a == 1):
    encode()

  elif (a == 2):
    print("Decoded Word : " + decode())
  else:
    raise Exception("Enter correct input")


if __name__ == '__main__' :
  main()

