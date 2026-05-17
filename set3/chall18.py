from Crypto.Cipher import AES
import struct
import base64

def xor_bytes(b1, b2):
     return bytes([a^b for a,b in zip(b1,b2)])

key = b"YELLOW SUBMARINE"
nonce = 0
ciphertext = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

cipher = AES.new(key, AES.MODE_ECB)
plaintext = b""

for i in range((len(ciphertext)+15) // 16):
    counter_block = struct.pack('<Q', nonce) + struct.pack('<Q', i)
    
    keystream_block = cipher.encrypt(counter_block)
    
    chunk = ciphertext[i*16 : (i+1)*16]
    plaintext += xor_bytes(chunk, keystream_block)
    
print(plaintext.decode())
