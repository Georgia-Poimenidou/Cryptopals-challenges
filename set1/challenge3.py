#Challenge 4 (S1C3)

hex_string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
binary_string = bytes.fromhex(hex_string)

#the scoring algorithm
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

#the main- XOR algorithm 
def find_text(binary_text):
    best_score = -1
    best_key = 0
    best_text = ''
    
    #brute forcing every possible key
    for possible_key in range(256):
        #XOR the key with the data
        current_bytes = bytes([possible_key ^ char for char in binary_text])
        current_score = get_score(current_bytes)
        
        #keep only the best_score everytime, that is the one that looks 'more English'
        if (current_score > best_score):
            best_score = current_score
            best_key = possible_key
            best_text = current_bytes.decode('ascii', errors='ignore')
            
    print('The key is ' + chr(best_key) + ' and the XORed string is: ' + best_text)   
    
find_text(binary_string)



