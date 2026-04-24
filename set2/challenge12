import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- Setup the Oracle ---
SECRET_KEY = b"YELLOW SUBMARINE" # In reality, this is unknown
UNKNOWN_STR = base64.b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdyBUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaSBEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnk="
)

def oracle(user_input):
    plaintext = user_input + UNKNOWN_STR
    # PKCS7 Padding
    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len] * pad_len)
    
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

# --- The Attack ---
def crack_ecb():
    block_size = 16
    decrypted_secret = b""
    
    # Calculate total length to decrypt (rounded up to block boundary)
    total_len = len(oracle(b""))
    
    for i in range(total_len):
        # 1. Create a prefix to shift the target byte to the end of a block
        # If we are looking for byte 0, padding is 15. For byte 1, padding is 14...
        padding_len = (block_size - 1 - (len(decrypted_secret) % block_size))
        prefix = b"A" * padding_len
        
        # 2. Get the "target" ciphertext block
        # We only care about the block where our "unknown" byte is currently at the end
        full_cipher = oracle(prefix)
        target_block_idx = len(decrypted_secret) // block_size
        target_block = full_cipher[target_block_idx*block_size : (target_block_idx+1)*block_size]
        
        # 3. Brute force the byte
        found = False
        for char_code in range(256):
            test_byte = bytes([char_code])
            # The test input consists of the prefix + what we've already decrypted + current guess
            test_input = prefix + decrypted_secret + test_byte
            res = oracle(test_input)
            
            # Compare the relevant block
            res_block = res[target_block_idx*block_size : (target_block_idx+1)*block_size]
            
            if res_block == target_block:
                decrypted_secret += test_byte
                found = True
                break
        
        if not found: # End of string/padding reached
            break

    return decrypted_secret

print(crack_ecb().decode())
