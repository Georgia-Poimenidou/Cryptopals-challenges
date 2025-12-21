import base64
from Crypto.Cipher import AES

key = b"YELLOW SUBMARINE"
url_data = "https://cryptopals.com/static/challenge-data/7.txt"

# Get the ciphertext you want to decode
with open("7.txt", "r") as f:
    ciphertext = base64.b64decode(f.read())
    
# Initialize the AES Cipher in ECB mode    
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt the data
decrypted_bytes = cipher.decrypt(ciphertext)

print(decrypted_bytes.decode('ascii'))
