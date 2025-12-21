import base64

with open("6.txt", "r") as f:
    ciphertext = base64.b64decode(f.read())

# Hamming distance
def hamming_distance(b1, b2):
    # XOR the bytes and count the 1's- the different bits
    return sum(bin(byte1 ^ byte2).count('1') for byte1, byte2 in zip(b1, b2))

# Solve Single byte XOR
# The scoring algorithm
def get_score(binary_text):
    score = 0
    #these letters represent roughly 70% of written English
    common_letters = 'ETAOIN SHRDLU'
    
    for byte in binary_text:
        #convert every byte to a capital character to check if it is one of the common letters
        char = chr(byte).upper()
        if char in common_letters:
            score += 1
    return score

# The main- XOR algorithm 
def solve_single_byte_xor(binary_text):
    best_score = -1
    best_key = 0

    #brute forcing every possible key
    for possible_key in range(256):
        #XOR the key with the data
        current_bytes = bytes([possible_key ^ char for char in binary_text])
        current_score = get_score(current_bytes)
        
        #keep only the best_score everytime, that is the one that looks 'more English'
        if (current_score > best_score):
            best_score = current_score
            best_key = possible_key

    return best_key


scores = []
for ks in range(2, 41):
    b1, b2, b3, b4 = ciphertext[0:ks], ciphertext[ks:ks*2], ciphertext[ks*2:ks*3], ciphertext[ks*3:ks*4]
    
    # Compute the average and normalized distance per keysize
    dist =  (hamming_distance(b1, b2) + hamming_distance(b2, b3) + hamming_distance(b3, b4)) / (3 * ks)
    
    scores.append((dist, ks))
    
# Take the best keysize- the one with the lowest score
best_keysize = sorted(scores)[0][1]
    
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

print(f"The hidden key is: {full_key}")

# Decrypt the original ciphertext
decrypted_message = ""
for i, byte in enumerate(ciphertext):
    # Cycle through the key
    key_byte = ord(full_key[i % len(full_key)])
    decrypted_message += chr(byte ^ key_byte)

print(decrypted_message)
