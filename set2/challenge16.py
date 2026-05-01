# Set 2, Challenge 16

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def pkcs7_padding(message, block_size):
    
    # Calculate how many bytes we need to add
    padding_len = block_size - (len(message) % block_size)
    
    # Create the padding bytes
    padding = bytes([padding_len]) * padding_len
    
    return message + padding

def encrypt_function(user_input, key, iv):

    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    
    safe_input = user_input.replace(b";", b"").replace(b"=", b"")
    
    plaintext = pkcs7_padding(prefix + safe_input + suffix, 16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    return encryptor.update(plaintext) + encryptor.finalize()
    
def decrypt_function(ciphertext, key, iv):
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) +decryptor.finalize()
    
    print(f"Decrypted Result: {plaintext}")
    return b";admin=true;" in plaintext

iv = os.urandom(16)
key = os.urandom(16)

user_payload = b"A" * 16 + b":admin<true:" 
ciphertext = bytearray(encrypt_function(user_payload, key, iv))

ciphertext[32] = ciphertext[32] ^ ord(':') ^ ord(';')
ciphertext[38] = ciphertext[38] ^ ord('<') ^ ord('=')
ciphertext[43] = ciphertext[43] ^ ord(':') ^ ord(';')

result = decrypt_function(bytes(ciphertext), key, iv)
print(f"Is Admin? {result}")
