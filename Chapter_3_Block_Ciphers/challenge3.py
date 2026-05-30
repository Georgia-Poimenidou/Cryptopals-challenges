# Set 1, Challenge 8

def count_repetitions(hex_string):
    ciphertext = bytes.fromhex(hex_string)
    
    # Break into 16-byte blocks
    chunks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    
    # Count how many are unique blocks with len(set(chunks)), the rest are duplicates
    number_of_duplicates = len(chunks) - len(set(chunks))
    
    return number_of_duplicates
    
with open("8.txt", "r") as f:
    for line_num, line in enumerate(f):
        line = line.strip()
        repeats = count_repetitions(line)
        
        if repeats > 0:
            print(f"Detected ECB on line {line_num}!")
            print(f"Found {repeats} repeated blocks.")
            print(f"Hex: {line[:30]}...")
