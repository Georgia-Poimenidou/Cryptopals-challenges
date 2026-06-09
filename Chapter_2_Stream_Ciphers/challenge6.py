# Set 1, Challenge 6

import base64

# Read and decode the base64 file
with open("6.txt", "r") as f:
    ciphertext = base64.b64decode(f.read())
    
def hamming_distance(b1, b2):
    return sum(bin(byte1 ^ byte2).count('1') for byte1, byte2 in zip(b1, b2))

# Scoring Algorithm
def get_score(binary_text):
    score = 0
    for byte in binary_text:
        if 32 <= byte <= 126 or byte in (9, 10, 13):
            char = chr(byte).lower()
            if char in 'etaoin shrdlu':
                score += 3    
            elif char.isalpha():
                score += 1    
            else:
                score += 0.5  
        else:
            score -= 5        
    return score

def solve_single_byte_xor(binary_text):
    best_score = float('-inf') 
    best_key = 0
    for possible_key in range(256):
        current_bytes = bytes([possible_key ^ char for char in binary_text])
        current_score = get_score(current_bytes)
        if current_score > best_score:
            best_score = current_score
            best_key = possible_key
    return best_key

# Keysize Calculation
scores = []
for ks in range(2, 41):
    # Split the entire ciphertext into chunks of 'ks' length
    blocks = [ciphertext[i:i+ks] for i in range(0, len(ciphertext), ks)]
    
    # Discard the last block if it's not fully 'ks' bytes long
    blocks = [b for b in blocks if len(b) == ks]
    
    dist_sum = 0
    # Compare every adjacent block in the entire file
    for i in range(len(blocks) - 1):
        dist_sum += hamming_distance(blocks[i], blocks[i+1])
        
    # Normalize the average distance
    dist = dist_sum / ((len(blocks) - 1) * ks)
    scores.append((dist, ks))
    
# Take the best keysize
best_keysize = sorted(scores)[0][1]

# Transpose the blocks based on the best keysize
piles = [[] for _ in range(best_keysize)]
for i, byte in enumerate(ciphertext):
    pile_index = i % best_keysize
    piles[pile_index].append(byte)

full_key = ""

# Solve single byte XOR for each pile
for pile in piles:
    pile_bytes = bytes(pile)
    key_char = solve_single_byte_xor(pile_bytes)
    full_key += chr(key_char)

print(f"The hidden key is: '{full_key}'")
print("-" * 50)

# Decrypt the original ciphertext
decrypted_message = ""
for i, byte in enumerate(ciphertext):
    key_byte = ord(full_key[i % len(full_key)])
    decrypted_message += chr(byte ^ key_byte)

print(decrypted_message)
