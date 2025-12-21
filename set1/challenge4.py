import requests

# URL for Cryptopals Challenge 4 data
url = "https://cryptopals.com/static/challenge-data/4.txt"
response = requests.get(url)
lines = response.text.splitlines()

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
def solve_line(hex_string):
    binary_text = bytes.fromhex(hex_string)
    best_local_score = -1
    best_local_key = 0
    best_local_text = ''
    
    #brute forcing every possible key
    for possible_key in range(256):
        #XOR the key with the data
        current_bytes = bytes([possible_key ^ char for char in binary_text])
        current_score = get_score(current_bytes)
        
        #keep only the best_score everytime, that is the one that looks 'more English'
        if (current_score > best_local_score):
            best_local_score = current_score
            best_local_key = possible_key
            best_local_text = current_bytes.decode('ascii', errors='ignore')
            
    return best_local_score, best_local_key, best_local_text

#open file

ultimate_best_score = -1
ultimate_best_key = 0
ultimate_best_text = ''

for line in lines:
    current_line_score, current_line_key, current_line_text = solve_line(line.strip())
    
    if current_line_score > ultimate_best_score:
        ultimate_best_score = current_line_score
        ultimate_best_key = current_line_key
        ultimate_best_text = current_line_text

print('The key is ' + chr(ultimate_best_key) + ' and the XORed hidden string is: ' + ultimate_best_text)

