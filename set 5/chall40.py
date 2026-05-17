# Set 5, Challenge 40

import random
from Cryptodome.Util.number import getPrime

# Use the helping functions of challenge 39
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

# Function to calculate the inger cube root of a number n 
def integer_cube_root(n):
    
    # Use binary search to find the exact integer cube root of n
    low = 0
    high = n
    while low < high:
        mid = (low+high) // 2
        if mid**3 <n:
            low = mid+1
        else:
            high = mid
    return low
        
# Function to simulate the RSA key generation
def generate_rsa_key():
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    return n, 3

print("Start of the communication")
message_int = int.from_bytes(b"Congrats you just implemented successfully a RSA broadcast attack!", byteorder='big')  
  
# Generate 3 different public keys
n1, e = generate_rsa_key()
n2, _ = generate_rsa_key()
n3, _ = generate_rsa_key()

# Encrypt the same message with all 3 keypairs
c1 = pow(message_int, 3, n1)
c2 = pow(message_int, 3, n2)
c3 = pow(message_int, 3, n3)

print("[Mallory] Intercepted c1, c2, c3 and knows n1, n2, n3.")

# Implement the Chinese Remainder Theorem to find the message
N_total = n1*n2*n3

# Calculate the m_i values (N_total divided by the specific n_i)
m1 = N_total // n1 
m2 = N_total // n2
m3 = N_total // n3

# Calculate the result C of the CTR formula
# Result = (c1*m1*invmod(m1, n1) + c2*m2*invmod(m2, n2) + c3*m3*invmod(m3, n3)) % N_total
part1 = c1*m1*invmod(m1, n1)
part2 = c2*m2*invmod(m2, n2)
part3 = c3*m3*invmod(m3, n3)

# C is the resulting huge number which is exactly equal to M^3
C = (part1+part2+part3) % N_total

# Calculate the cube root
recovered_int = integer_cube_root(C)

# Convert the recovered message back to text 
recovered_bytes = recovered_int.to_bytes((recovered_int.bit_length() + 7) // 8, byteorder='big')
print(f"[Mallory] Recoved the message: {recovered_bytes.decode()}")