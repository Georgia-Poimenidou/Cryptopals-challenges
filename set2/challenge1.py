def pkcs7_padding(message, block_size):
    
    # Calculate how many bytes we need to add
    padding_len = block_size - (len(message) % block_size)
    
    # Create the padding bytes
    padding = bytes([padding_len]) * padding_len
    
    return message + padding
    
# Test the example from the challenge
original = b"YELLOW SUBMARINE"
padded = pkcs7_padding(original, 20)

print(f"Original: {original}")
print(f"Padded:   {padded}")
