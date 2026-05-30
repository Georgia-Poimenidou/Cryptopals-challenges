# Set 3, Challenge 22

import time
import random

# Use the MT19937 class implementation from Challenge 21
class MT19937:
    def __init__(self, seed):
        self.MT = [0] * 624
        self.index = 624
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = (1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i) & 0xFFFFFFFF

    def extract_number(self):
        if self.index >= 624:
            self.twist()
        y = self.MT[self.index]
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= (y >> 18)
        self.index += 1
        return y & 0xFFFFFFFF

    def twist(self):
        for i in range(624):
            x = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % 624] & 0x7FFFFFFF)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= 0x9908B0DF
            self.MT[i] = self.MT[(i + 397) % 624] ^ xA
        self.index = 0

# The routine simulating the vulnerability
def get_random_token():
    # Get current real Unix timestamp
    start_time = int(time.time())
    
    # Wait a random number of seconds between 40 and 1000.
    seed_time = start_time + random.randint(40, 1000)
    
    # Initialize the MT19937 PRNG with the Unix timestamp
    rng = MT19937(seed_time)
    
    # Wait a random number of seconds again
    output_time = seed_time + random.randint(40, 1000)
    
    # Extract the first 32 bit output
    token = rng.extract_number()
    
    print(f"[System] Token generated! True hidden seed was: {seed_time}")
    return token, output_time

# Simulate the attacker brute forcing the seed
def crack_timestamp_seed(target_token, intercept_time):
    print(f"\n[Attacker] Intercepted token: {target_token} at unix time: {intercept_time}")
    print("[Attacker] Scanning past timestamps for a matching seed...")
    
    # We know the token was generated in the past.
    # The maximum total sleep time was 1000 + 1000 = 2000 seconds.
    # So we search from (intercept_time - 2000) up to intercept_time.
    for guessed_seed in range(intercept_time - 2000, intercept_time):
        test_rng = MT19937(guessed_seed)
        
        # Check if this guessed seed produces the target token
        if test_rng.extract_number() == target_token:
            return guessed_seed
            
    return None

# Run the challenge
token, intercept_time = get_random_token()
discovered_seed = crack_timestamp_seed(token, intercept_time)

if discovered_seed:
    print(f"SUCCESS! Exploit cracked the seed: {discovered_seed}")
else:
    print("Exploit failed.")
