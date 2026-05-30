#Set 1, Challenge 2

def XOR(s1:str, s2 :str) ->str:
    b1 = bytes.fromhex(s1)
    b2 = bytes.fromhex(s2)
    
    res = bytes([x ^ y for x,y in zip(b1, b2)])
    
    return res.hex()
    
#Test code
s1 = '1c0111001f010100061a024b53535009181c'
s2 = '686974207468652062756c6c277320657965'

res = XOR(s1,s2)
print(res)
