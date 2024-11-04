import base64
import random as r
import sys
sys.set_int_max_str_digits(0)
with open("your_image.jpg", "rb") as image2string:
    converted_string = base64.b64encode(image2string.read())

with open('encode.bin', "wb") as file:
    file.write(converted_string)

def convert_base64_to_base2(base64_string):
  """Converts a base 64 string to a base 2 string.

  Args:
    base64_string: The base 64 string to convert.

  Returns:
    The base 2 string.
  """

  byte_array = base64.decodebytes(base64_string)
  binary_strings = []
  for byte in byte_array:
    binary_strings.append(bin(byte)[2:].zfill(8))
  return "".join(binary_strings)

# Example usage:
base2_string = convert_base64_to_base2(converted_string)



def calculate_parity_bits(data):
    n = len(data)
    m = 0
    while 2 ** m <= n + m + 1:
        m += 1
    encoded_data = [''] * (n + m)
    j = 0
    k = 0

    for i in range(1, n + m + 1):
        if i == 2 ** k:
            encoded_data[i - 1] = 'p'
            k += 1
        else:
            encoded_data[i - 1] = data[j]
            j += 1

    for i in range(m):
        mask = 2 ** i
        parity = 0
        for j in range(1, n + m + 1):
            if j & mask:
                if encoded_data[j - 1] == '1':
                    parity = parity ^ 1
        encoded_data[(2 ** i) - 1] = str(parity)

    return ''.join(encoded_data)


def hamming_decode(encoded_data):
    n = len(encoded_data)
    m = 0
    while 2 ** m <= n:
        m += 1
    parity_bits = []

    for i in range(m):
        mask = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & mask:
                if encoded_data[j - 1] == '1':
                    parity = parity ^ 1
        parity_bits.append(str(parity))

    error_index = int(''.join(reversed(parity_bits)), 2)
    if error_index != 0:
        print("Error at position:", error_index)
        corrected_encoded_data = list(encoded_data)
        corrected_encoded_data[error_index - 1] = str(
            int(corrected_encoded_data[error_index - 1]) ^ 1)
        encoded_data = ''.join(corrected_encoded_data)
        print("Corrected data:", encoded_data)
    else:
        print("No error detected.")

    decoded_data = ''
    j = 0
    for i in range(1, n + 1):
        if i != 2 ** j:
            decoded_data += encoded_data[i - 1]
        else:
            j += 1
    return decoded_data

def errorgenerator(hammingcode):
    for i in range(0,int(len(hammingcode)/7)):
        hamminglist=list(hammingcode)
        k=7*i+int(r.random()*7)
        print(k)
        t=r.random()
        print(t)
        if(t<0.33):
            hamminglist[k]='0'
        if(t>0.67):
            hamminglist[k]='1'
    
    return ''.join([str(bit) for bit in hamminglist])


def convert_base2_to_base64(base2_string):
  """Converts a base 2 string to base 64.

  Args:
    base2_string: A string of 0s and 1s.

  Returns:
    A base 64 encoded string.
  """

  # Convert the base 2 string to a bytes object.
  bytes_object = bytes([int(base2_string[i:i + 8], 2) for i in range(0, len(base2_string), 8)])

  # Encode the bytes object to base 64.
  base64_encoded_string = base64.b64encode(bytes_object)

  # Return the base 64 encoded string.
  return base64_encoded_string

encoded_data = calculate_parity_bits(base2_string)
print("Hamming code:") 
print( encoded_data)
decoded_data = hamming_decode(encoded_data)
print("Decoded data:", decoded_data)

encoded_witherror=errorgenerator(encoded_data)
print(encoded_witherror)

print("this is the difference due to the error")
print((encoded_witherror==encoded_data))



base64_encoded_string1 = convert_base2_to_base64(decoded_data)
base64_encoded_string2=convert_base2_to_base64(hamming_decode(encoded_witherror))
base64_error_string=convert_base2_to_base64(errorgenerator(base2_string))


with open('decoded.bin', "wb") as file:
    file.write(base64_encoded_string1)

with( open('error_file.bin',"wb")) as file:
    file.write(base64_error_string)

with open('error_decoded.bin','wb') as file:
    file.write(base64_encoded_string2)

file1= open('decoded.bin', 'rb') 
file2=open('error_decoded.bin','rb')
byte1 = file1.read() 
byte2 = file2.read()
errorbyte=open('error_file.bin').read()
file1.close() 
file2.close()
  
decode1 = open('image_reconstructed.jpeg', 'wb')
decode1.write(base64.b64decode((byte1))) 
decode1.close() 


error=open("image_with_error.jpeg",'wb')
error.write(base64.b64decode(errorbyte))

decode2=open('image_fixed.jpeg','wb')
decode2.write(base64.b64decode((byte1)))