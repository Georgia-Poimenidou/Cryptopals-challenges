# Extra Challenge, Chapter 3

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def pkcs7_padding(message, block_size):
    
    # Calculate how many bytes we need to add
    padding_len = block_size - (len(message) % block_size)
    
    # Create the padding bytes
    padding = bytes([padding_len]) * padding_len
    
    return message + padding

def pkcs7_unpad(message):
    padding_len = message[-1]
    return message[:-padding_len]

def encrypt_function(user_input, key, iv):

    prefix = b"admin=0;user="
    suffix = b";session=active"
    
    safe_input = user_input.replace(b";", b"").replace(b"=", b"")
    
    plaintext = pkcs7_padding(prefix + safe_input + suffix, 16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    return iv + ciphertext
    
def decrypt_function(token, key):
    
    iv = token[:16]
    ciphertext = token[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext_padded = decryptor.update(ciphertext) +decryptor.finalize()
    
    plaintext = pkcs7_unpad(plaintext_padded)
    print(f"Server decrypted result: {plaintext}")
    
    # Check if we successfully forged the admin parameter
    return b"admin=1" in plaintext

def forge_iv_token(intercepted_token):
    mutable_token = bytearray(intercepted_token)
    
    index_to_flip = 6
    
    mutable_token[index_to_flip] ^= ord('0') ^ ord('1')
    
    return bytes(mutable_token)
    
# Implementation of the attack
if __name__ == "__main__":
    # Server generates a random key for the session
    MASTER_KEY = os.urandom(16)
    
    # Server generates a random IV for this specific login
    session_iv = os.urandom(16)
    original_token = encrypt_function(b"bob", MASTER_KEY, session_iv)
    print(f"Original Token (Hex): {original_token.hex()}")
    
    # Create the token that the attacker forges
    forged_token = forge_iv_token(original_token)
    
    # Server verifies forged token 
    is_admin = decrypt_function(forged_token, MASTER_KEY)
    
    if is_admin:
        print("SUCCESS: Admin privileges granted via IV manipulation!")
    else:
        print("FAILURE: Access denied.")
