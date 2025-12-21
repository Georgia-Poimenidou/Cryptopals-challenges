# Set 1, Challenge 1

from base64 import b64encode, b64decode

def hex2base64(hex_string: str) -> str:
    return b64encode(bytes.fromhex(s)).decode()

# Test code
s = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
b64 = hex2base64(s)
print(b64)