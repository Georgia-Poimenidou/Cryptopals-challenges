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
  
e = 3  
d = -1
# Define the RSA parameters
while d == -1:
    p = generate_prime(100, 500)
    q = generate_prime(100, 500)
    
    if p ==q:
        continue
     
    n = p*q
    et = (p-1)*(q-1)
     
    d = invmod(e, et)
     
print(f"Public Key: ({n}, {e})")
print(f"Private Key: ({n}, {d})")

#Define a message
m = 42
print(f"Original Message: {m}")

# Encrypt the message
c = pow(m, e, n)
print(f"Ciphertext: {c}")

# Decrypt the message
decrypted_m = pow(c, d, n)
print(f"Decrypted Message: {decrypted_m}")
print(f"Success: {m == decrypted_m}")