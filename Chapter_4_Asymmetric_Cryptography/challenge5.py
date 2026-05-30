# Set 5, Challenge 34

import random
import hashlib
import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

def derive_key(secret_int):
    # Convert the math secret to bytes, hash it with SHA1, and take the first 16 bytes for AES
    s_bytes = secret_int.to_bytes((secret_int.bit_length() + 7) // 8 or 1, byteorder='big')
    return hashlib.sha1(s_bytes).digest()[:16]

def encrypt_msg(key, msg):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(msg, 16))
    return ciphertext + iv  # Append IV to the end as requested by your pseudo-code

def decrypt_msg(key, payload):
    iv = payload[-16:]      # Extract the last 16 bytes for the IV
    ciphertext = payload[:-16] # The rest is the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), 16)

# A -> M : Alice sends her public key (not knowing that Mallory listens to the communication)
p = 37
g = 5
a = random.randint(1, p-1)
A = pow(g,a,p)  

# M -> B : Mallory intercepts the communication and send a fake A to Bob
fake_A = p
print("[Mallory] Intercepted Alice's A. Forwarding 'p' to Bob.")

#B -> M : Bob receives Mallory's fake key (thinking that it is Alice's)
b =  random.randint(1, p-1)
B = pow(g,b,p)

# M -> A : Mallory intercepts the communication and send a fake B to Alice
fake_B = p
print("[Mallory] Intercepted Bob's B. Forwarding 'p' to Alice.")

# Alice computes her shared secret using fake_B (which is p)
alice_secret = pow(fake_B, a, p)
alice_key = derive_key(alice_secret)

# A -> M : Alice sends a secret message to the communication channel (where Mallory listens)
msg_from_alice = b"Hello Bob!"
alice_payload =  encrypt_msg(alice_key, msg_from_alice)
print(f"[Alice] Sent encrypted payload: {alice_payload.hex()[:30]}...")

# M -> B : Mallory relays the message to Bob
mallory_secret = 0 # Mallory knows that since she injected 'p', the secret is 0, because B^a % p = p^a%p = 0
mallory_key = derive_key(mallory_secret)
mallory_stolen_msg1 = decrypt_msg(mallory_key, alice_payload)
print(f"[Mallory] STOLEN FROM ALICE: {mallory_stolen_msg1.decode()}")

# Bob receives the payload from Mallory (thinking it's from Alice)
bob_secret = pow(fake_A, b, p) # p^b % p is also 0!
bob_key = derive_key(bob_secret)

# B -> M : Bob sends a secret message to the communication channel (where Mallory listens)
bob_decrypted_msg = decrypt_msg(bob_key, alice_payload)
print(f"[Bob] Received and decrypted: {bob_decrypted_msg.decode()}")

msg_from_bob = b"Hello Alice!"
bob_payload = encrypt_msg(bob_key, msg_from_bob)
print(f"\n[Bob] Sent encrypted reply: {bob_payload.hex()[:30]}...")

# M -> A : Mallory relays the message to Alice

mallory_stolen_msg2 = decrypt_msg(mallory_key, bob_payload)
print(f"[Mallory] STOLEN FROM BOB: {mallory_stolen_msg2.decode()}")

# Alice reveives the reply 
alice_decrypted_reply = decrypt_msg(alice_key, bob_payload)
print(f"[Alice] Received and decrypted: {alice_decrypted_reply.decode()}")
