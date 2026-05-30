# Learning Cryptography Through Cryptopals

This repository contains the complete Python source code and challenge solvers accompanying my BSc Thesis: **"Learning cryptography through cryptopals.com"**. 

While the thesis focuses on the mathematical foundations and theoretical vulnerabilities of modern encryption, this repository provides the hands-on, executable exploits. It is designed to bridge the gap between abstract cryptographic concepts and practical cybersecurity engineering.

## 🚀 Repository Structure

The code is organized sequentially to match the chapters of the thesis, progressing from basic bitwise operations to advanced public-key exploitation.

### **`Chapter_2_Stream_Ciphers/`** *Focuses on Encoding, XOR mechanics, Frequency Analysis, and Many-Time Pad attacks.*
* **Challenge 2.1 (S1C1):** Hex to Base64 Conversion
* **Challenge 2.2 (S1C2):** Fixed XOR Operation
* **Challenge 2.3 (S1C5):** Repeating-key XOR Encryption
* **Challenge 2.4 (S1C3):** Single-byte XOR Decryption
* **Challenge 2.5 (S1C4):** Detect Single-character XOR
* **Challenge 2.6 (S1C6):** Break Repeating-key XOR
* **Challenge 2.7 (S3C19):** Break the fixed-nonce CTR
* **Extra Challenge 1:** Decrypting an Over-XOR'd Message

### **`Chapter_3_Block_Ciphers/`**
*Focuses on AES-128 in ECB/CBC modes, Padding Oracles, and Bit-flipping attacks.*
* **Challenge 3.1 (S2C9):** PKCS#7 Padding
* **Challenge 3.2 (S2C10):** CBC Mode Implementation
* **Challenge 3.3 (S1C8):** Detect AES in ECB Mode
* **Challenge 3.4 (S2C12):** Byte-at-a-time ECB Decryption
* **Challenge 3.5 (S2C16):** CBC Bit-flipping Attack
* **Challenge 3.6 (S3C17):** The CBC Padding Oracle
* **Extra Challenge 2:** The Unauthenticated IV Injection

### **`Chapter_4_Asymmetric_Cryptography/`**
*Focuses on PRNG entropy, Diffie-Hellman parameters, and RSA mathematical exploits.*
* **Challenge 4.1 (S3C21):** Implement MT19937 PRNG
* **Challenge 4.2 (S5C33):** Implement Diffie-Hellman
* **Challenge 4.3 (S6C39):** Implement RSA
* **Challenge 4.4 (S3C22):** Crack an MT19937 Seed
* **Challenge 4.5 (S5C34):** Diffie-Hellman MITM Attack
* **Challenge 4.6 (S6C40):** RSA Broadcast Attack
* **Extra Challenge 3:** The RSA Blinding Attack

## 🛠️ How to Use
All solvers are written in Python 3. To execute a specific challenge, navigate to its respective directory and run the python script. 

*Note: The code prioritizes readability and pedagogical value over hyper-optimization, mirroring the educational goals of the thesis.*
