# Set 3, Challenge 17

import os
import random
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def pkcs7_padding(message, block_size):
    
    # Calculate how many bytes we need to add
    padding_len = block_size - (len(message) % block_size)
    
    # Create the padding bytes
    padding = bytes([padding_len]) * padding_len
    
    return message + padding

def encrypt_function(key, iv):
    strings = [ "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93" ]
        
    # Select a random string from the given strings
    plaintext = base64.b64decode(random.choice(strings)) 

    # Pad the chosen string
    plaintext = pkcs7_padding(plaintext, 16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    return encryptor.update(plaintext) + encryptor.finalize()
    
def decrypt_function(ciphertext, key, iv):
    
    #Decrypt the ciphertext using AES
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) +decryptor.finalize()
        
    #Take the last value of the plaintext, that is the padding value
    padding_len = plaintext[-1]
    
    # Check if padding is between 1 and 15
    if padding_len == 0 or padding_len >16:
        return False
    
    # Extract the padding from the ciphertext
    actual_padding = plaintext[-padding_len:]
    
    # Calculate the expected padding
    expected_padding = bytes([padding_len] * padding_len)
    
    return actual_padding == expected_padding

def padding_oracle_solver(ciphertext, iv, key):
    # This function mimics an attacker who does not know the key.
    # It only uses decrypt_function(modified_data, key, iv)
    
    blocks = [iv] + [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    final_plaintext = b""

    # Process each block
    for b in range(1, len(blocks)):
        c_prev = blocks[b-1]
        c_curr = blocks[b]
        
        intermediate = [0] * 16
        decoded_block = [0] * 16

        # Loop through each byte in the block (15 down to 0)
        for i in range(15, -1, -1):
            pad_val = 16 - i
            
            # Prepare the suffix of the modified block based on bytes we already found
            suffix = bytes([intermediate[j] ^ pad_val for j in range(i + 1, 16)])
            
            for guess in range(256):
                # Build a fake 'previous' block
                test_c_prev = os.urandom(i) + bytes([guess]) + suffix
                
                # Ask the Oracle: "Is this padding valid?"
                if decrypt_function(test_c_prev + c_curr, key, os.urandom(16)):
                    # If True, we found the intermediate byte
                    intermediate[i] = guess ^ pad_val
                    decoded_block[i] = intermediate[i] ^ c_prev[i]
                    break
        
        final_plaintext += bytes(decoded_block)
    
    return final_plaintext

iv = os.urandom(16)
key = os.urandom(16)

ciphertext = encrypt_function(key, iv)

# Execute the attack
print("Starting Attack...")
attack_result = padding_oracle_solver(ciphertext, iv, key)
print(f"Decrypted without knowing the key: {attack_result}")
     
