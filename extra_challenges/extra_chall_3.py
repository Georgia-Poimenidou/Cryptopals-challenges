import random    

def is_prime(a):
    if a < 2:
        return False
    for i in range(2, int(a**0.5)+1):
        if a % i == 0:
            return False
    return True
        
def generate_prime(min, max):
    while True:
        p = random.randint(min, max)
        if is_prime(p):
            return p

def egcd(a,b):
    # The base case of the recursion
    if (a == 0):
        return b, 0, 1
    
    # Use recursion to keep track of the coefficients
    gcd, x1, y1 = egcd(b%a, a)
    
    # gcd = x*a + y*b
    x = y1 - (b//a) *x1 # b//a is the quotient of the division, that is q in the expression b = a * q + r
    y = x1
    
    return gcd, x, y

def invmod(e, phi):
    gcd, x, y = egcd(e, phi)
    
    if gcd != 1: # That means that the numbers are not relatively prime so e doesn't have inverse mod phi
        return -1
    else: # Ensure that the value that returns is positive
        return x%phi
  
# Function to simulate the RSA keys generation
def generate_rsa_keys():
    p = generate_prime(1000, 5000)
    q = generate_prime(1000, 5000)
    n = p * q
    phi = (p-1)*(q-1)
    
    e = 65537
    d = invmod(e, phi)
    return n, e, d
  
def RSA_encrypt(m, e, n):
    return pow(m, e, n)
    
def RSA_decrypt(c, d, n, blacklist):
        
    if c not in blacklist: 
        return pow(c, d, n)
    else:
        print("SERVER FIREWALL EROR: Blacklisted Cipherxt Detected!")
        return -1
  
def create_blacklisted_C():
    
    n, e, d = generate_rsa_keys()
    secret_msg = int.from_bytes(b"WIN", 'big')    
    blacklisted_C = pow(secret_msg,e,n)
    
    return blacklisted_C, n, e, d
    
# Implementation of the attack

# Take a blacklisted ciphertext 
blacklisted_C, n, e, d = create_blacklisted_C()

server_blacklist = [blacklisted_C]

# Generate a random number R
R = random.randint(2, 100)

 # Build a disguise C' = C*R^e (mod n)
blinded_C = (blacklisted_C * pow(R,e,n)) % n 
print(f"Blinded Ciphertext sent to server: {blinded_C}\n")

# Decrypt C'
blinded_M = RSA_decrypt(blinded_C, d, n, server_blacklist)

# Calculate original M 
if blinded_M != -1:
    R_inv = invmod(R, n)
    M_int = (R_inv* blinded_M) % n
    
    M_bytes = M_int.to_bytes((M_int.bit_length() + 7) // 8, 'big')
    print(f"\nOriginal message is: {M_bytes.decode('ascii')}")
