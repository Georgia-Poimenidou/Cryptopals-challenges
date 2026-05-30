#Set 1, Challenge 5

text = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''
byte_text = text.encode('utf-8')

key_text = 'ICE'
byte_key = key_text.encode('utf-8')

# use a list to store the resulting numbers (bytes)
encrypted_bytes = []

# use a pointer to indicate the byte character of the key to XOR each time with the byte_text character
pointer = 0 
# XOR the bytes and append the resulting number to the list
for byte in byte_text:
    encrypted_bytes.append(byte ^ byte_key[pointer])
    
    # cycle the pointer to point every time at the next character of the key
    pointer = (pointer + 1) % len(byte_key)

# convert the list of numbers to hex
encrypted_hex = bytes(encrypted_bytes).hex()
    
print(encrypted_hex)

