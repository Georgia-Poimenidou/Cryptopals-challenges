💡Here you can find the **explanation of the solver code** for every challenge:


<details>
  <summary><b>📂 Click to expand: Challenge 3 Write-up (Single-byte XOR) </b></summary>
  
  ## Write- Up of Challenge 3
  
  🎯 In this challenge we are searching for one single character that if XORed with the hex string given, produces an english string that makes sense. 

  The easiest approach is the brute force approach. Since we are searching for one character or one byte, that is 8 bits, so there are only 256 possible keys. The possible key is between 0 to 255. This is a small enough number that a computer can check every single one in a fraction of a millisecond. 
    
  Before starting, we must prepare our data to be processed. Hex strings are not convenient to be processed, so we first need to convert the hex string to bytes to be able to XOR it with the possible keys. In python there is a built-in faction to do so: bytes.fromhex(). This way we have created the binary_text string. 
    
  Now that we have our data in bytes format we can build the algorithm. We need to create a loop that will try all the possible keys XORed with our binary_text and keep the one that makes sense. How do we define ‘makes sense’? In English there are some letters that are most frequently used and thus if we spot them in our XORed string then there is a high possibility that our string is indeed the plaintext we are looking for. The challenge description helps us on that as well, the "ETAOIN SHRDLU" that it mentions in the end is the approximate order of frequency of the most common letters in English (based on old Linotype machine keyboards). In simple words, the most frequently used letter in English is ‘E’, then it’s ‘T’, ‘A’, and so on.
    
  We need to ‘devise a method for scoring a piece of English plaintext’ as the challenge description indicates. In our loop, we are going to count the appearances of the common letters ("ETAOIN SHRDLU") and keep this value in the variable current_score. We only care about counting the common letters because those are the ones that will indicate if the produced text is an english text. Think of it like a metal detector. If you walk across a field looking for gold, your detector only "beeps" when it hits gold. It ignores the dirt, the grass, and the rocks because those don't help you find the treasure. In this case, the English language is the treasure, and the gibberish is the dirt. When we XOR a hex string with a random key (like 5 or 127), the result is usually complete nonsense. It looks like this: ‘^!¡*ùå_?’. Our code looks at this nonsense and asks ‘Does this have any 'e's? Any 't's? Any spaces?’. If the answer is no, the current_score stays 0, that means we only found gibberish. Else, it adds 1 to the current_score for every common letter found. In each current_text produced there are going to be some common letters, but we want to find the best_text, that is the string with the most common letters because that’s the most possible one to be our desired plaintext. We will do that by keeping the best_score found so far in each loop and comparing it every time with the current_score. At the end of the loop, our algorithm has kept the best_score, the best_key that produced this score and the best_text that was produced by XORing the initial data with the best_key. 
    
  🔑 By decoding the byte-array in ascii and printing it, we see that the key is the character ‘X’ and the XORed string is: ‘Cooking MC's like a pound of bacon’.
     
</details>

<details>
  <summary><b>📂 Click to expand: Challenge 4 Write-up (Detect single-character XOR) </b></summary>
  
  ## Write- Up of Challenge 4
  
  🎯 In this challenge we are given a file with lines of 60-character hex-strings and we need to find the one string that has been encrypted by single-character XOR.    
  
  In simple words, we need to do the same as in the previous challenge, just this time instead of having one string we have a lot of strings of which only one will make sense. So we need to do what we did in the previous challenge for every line of the file given, keep the best_key and best_score of the line tested and then compare it to the rest to find the best of the best key and score. 

  Building up on our already written code of challenge 3, we will add a second loop and nest the already written one inside. We are going to iterate over each line trying all the 256 possible keys, keeping the one that if XORed with the line looks ‘more English’ and its score. This is the best_local_key and the best_local_score, which we are going to compare with the ultimate_best_score. At the end of the outer loop, we will end up with the only string/line that was XORed with a single character. 

  🔑 By decoding the byte-array in ascii and printing it, we see that the key is the character ‘5’ and the hidden XORed string is: ‘Now that the party is jumping’.

</details>
