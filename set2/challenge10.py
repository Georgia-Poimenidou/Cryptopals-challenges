# Set 2, Challenge 10

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

def aes_128_ecb_decrypt(ciphertext_block, key):
    #Encrypts one block of 16 bytes using AES-128 in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext_block) + decryptor.finalize()

def decrypt_cbc(ciphertext, key, iv):
    prev_block = iv
    plaintext = b""
    
    # Process one block of 16 bytes at a time
    for i in range(0, len(ciphertext), 16):
        current_block = ciphertext[i:i+16]
        
        # Step 1: Decrypt the block using ECB mode
        decrypted_block = aes_128_ecb_decrypt(current_block, key)
        
        # Step 2: XOR with the previous ciphertext block
        output_block = xor_bytes(decrypted_block, prev_block)
        
        plaintext += output_block
        
        # Step 3: Update prev_block for the next iteration
        prev_block = current_block
        
    return plaintext
    
key = b"YELLOW SUBMARINE"
iv = b"\x00" * 16  # Το IV είναι 16 μηδενικά bytes
    
# Φόρτωση και Base64 decoding του αρχείου
with open("ciphertext_chall10.txt", "r") as f:
    ciphertext = base64.b64decode(f.read())
    
# Εκτέλεση της αποκρυπτογράφησης
decrypted_message = decrypt_cbc(ciphertext, key, iv)
    
print("Decrypted Message:")
print(decrypted_message.decode('ascii'))
