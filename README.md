# DNAcodeX
DNAcodeX is a Python implemented software that can be executed through the command line. It was designed to map digital data to DNA sequences in addition to the employment of Huffman coding for compression and the incorporation of Hamming error correcting code to fix possible substitution errors that might be introduced to the DNA sequences during any step of the DNA data storage process. Similarly, as part of the DNAcodeX code, the decoder is responsible for examining the sequence
that had been encoded using DNAcodeX and for fixing and reporting substitution errors if present, in addition to the removal of the Hamming correcting redundancy data after performing the correction process.

If compression with Huffman coding was used, the user must indicate that during the decoding pro- cess. The decoder identifies and decodes the header part and constructs the Huffman dictionary that is specific to the content of the encoded file. After decoding the sequence using the constructed Huffman dictionary, data would be saved in a file with the format specified by the user and that too should be consistent with the format of the file before the encoding process.
In addition to compression and the correction of substitution errors, DNAcodeX is compatible with  the UTF-8 encoding system, which enables DNAcodeX to encode up to 1,112,064 different characters.

Python (version 3.10.12) programming language was used to develop the code of two scripts that together constitute DNAcodeX. The first script DNAcodeX_encoder.py includes all the functions necessary for reading different file formats, converting data to binary, compressing data, adding error correcting bits and encoding data into DNA sequences. The second script DNAcodeX_decoder.py is used for decoding DNA sequences that carry data encoded by the DNAcodeX encoder program.
Using the library argparse, the arguments that are needed for the scripts to be executed by the
command-line were defined.

DNAcodeX is structured around four core pillars:
1. Encoding and decoding texts that use UTF-8 characters and other file formats (i.e., images,
compressed files).
2. The compression of data using Huffman coding.
3. Detecting and correcting single base substitution errors using Hamming errors correcting rules.
4. Mapping binary to DNA bases (encoding) and DNA bases to binary (decoding).

    - 1 is mapped to G and 0 is mapped to C. Then DNAcodeX loops through the GC sequence
    and for each even position: if the base is C it gets converted to T, and if the base is G it
    gets converted to A.

    **Note** : There are two reasons for this mapping:
    
        - Since Gs and Cs are converted to As and Ts respectively, errors that substitute A bases with G bases or T bases with C bases are not actually considered errors            as they represent the same bit when the sequence is converted to binary. This mapping method adds up to the robustness of DNAcodeX when correcting                         single base substitution errors.
    
        - To diversify the composition of the sequence.

    - For the decoding process As and Ts are first converted to Gs and Cs respectively. Then,
    G is mapped to 1 and C is mapped to 0.


## UTF-8 and other file formats
UTF-8 is a method for encoding Unicode characters (which represent characters from various languages and symbols) into a sequence of 8-bit bytes. This means that each character is represented using a combination of 8 bits (1 byte) or multiple bytes, depending on the character’s codepoint. By comparison, ASCII (American Standard Code for Information Interchange) includes encodings for only 128-characters.
In UTF-8, when a character needs more than one byte to be represented, the first byte is called a
”leading byte.” The leading byte starts with a specific pattern of bits that indicates how many bytes will follow to complete the character’s representation, as illustrated bellow:
- 0xxxxxxx ----> 1 byte character
- 110xxxxx 10xxxxxx ----> 2 bytes character
- 1110xxxx 10xxxxxx 10xxxxxx ----> 3 bytes character
- 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx ----> 4 bytes character

DNAcodeX encodes multiple file formats (texts, images, and compressed files) by converting data to its binary representation, and then mapping to DNA bases. However, to decode the sequences that have UTF-8 characters, DNAcodeX first converts DNA bases to binary, then it goes through the binary data 8 bits at the time. By recognising the patterns of the first few bits (in the leading byte), DNAcodeX determines how many bytes should be interpreted together for a character to be decoded.

## Implementing Huffman Coding
Huffman compression algorithm was adopted for DNAcodeX to make the data smaller in size. Huffman coding is a lossless algorithm, meaning that there is no loss of information after compression. It works by assigning codes to characters based on their frequency in the data string.

To implement Huffman in Python, a class named node was coded to store each node’s attributes of the Huffman tree. Each node has attributes for the character (char), frequency (freq), and references to the left and right children (left, right). Then using build_frequency_table() function, the encoder takes a data string as input and return a dictionary containing the frequency of each character in the string. After that, a tree is built using the function build_huffman_tree() and attributes for each node are stored. Then a function named build_huffman_codes() takes the root node of the Huffman tree, a current code string, and an empty dictionary to store Huffman codes. The same function traverses the tree recursively, and for each leaf node, stores its character and the accumulated code in the dictionary. Finally, the encoder iterates through the characters of the input data string and appends the corresponding Huffman code to the encoded text.

As a result of the previous process, DNAcodeX generates a header that contains two elements in binary: 1. A string that tells the decoder the length of the Huffman dictionary. 2. Huffman dictionary that includes the characters and the corresponding codes separated by commas. The header (prelude) that contains the necessary information for decoding, is stored in the DNA sequence (after mapping to DNA bases) followed by the payload.

For the decoding process, DNAcodeX reads the Huffman dictionary stored in the header part of the payload, constructs the Huffman tree, iterates through each bit in the encoded string (after mapping DNA bases to binary), traverses the Huffman tree accordingly (left for ’0’ and right for ’1’), and appends the character of the leaf node to the decoded text.

## Implementing Hamming Error Correction

DNAcodeX uses Hamming codes to correct possible single substitutions that might occur in the encoded DNA sequences. The following paragraphs explain the concept of the Hamming codes as implemented for DNAcodeX.

For a string of bits, an error could be a bit-flip. For example, we might have a string of bits 01001. An error in the fourth bit would flip 0 to 1, resulting in the new message 01011. Error correction codes locate this error and correct it. This is achieved by taking a string of bits, as the input. Then, additional bits that are called parity bits are added to help in detecting and correcting errors.

DNAcodeX uses the XOR operation to calculate parity bits and incorporate them into the sequences. XOR (exclusive or) is represented by the symbol ⊕ and is a logical operator so that for two bits, if they are the same the result is 0. Whereas, if they are different the result is 1. For example, for the two-bits message 10: 1 ⊕ 0 = 1.

By adding a parity bit at the end, calculated from the first two bits, the new encoded message would be 101. If an error occurs to any of those three bits, the parity bit would be different if we recalculate it after the error. For example, for the original message 101, if an error occurs and the second bit is flipped, the message becomes 111. By recalculating the parity bit using the XOR operation: 1 ⊕ 1 = 0. Since the result of this calculation no longer matches the parity bit of the message, it can be concluded that an error has occurred to the message. However, in this case the error can not be corrected since the position is not known. For this reason, more rules are needed to both detect and correct the error.

Using this concept of calculating parity bits with the XOR operator, we combine multiple bits and append 3 parity bits, a binary string of the length 4 can be corrected for errors. This is called Hamming (7, 4), and is adopted for DNAcodeX.

Hamming (7, 4) takes in four-bit input and using the XOR operator it generates 3 parity bits and encodes the input into a seven-bit codeword. By calling the original bits of the message B1, B2, B3, B4 and the parity bits X1, X2, X3, the codeword would be B1B2B3B4X1X2X3, and the applied rules are as follows:
- X1 = B1 ⊕ B2 ⊕ B4
- X2 = B1 ⊕ B3 ⊕ B4
- X3 = B2 ⊕ B3 ⊕ B4

With those parity bits, the occurred error can be determined and corrected. However, it must be assumed that at most, a single bit error has occurred. If more than one error occurs, the code would end up correcting a different bit.

Assuming at most one error has occurred, those parity bits can be used to correct the error by checking for eight different cases. One for no error, and one for each of the seven bits of the encoded message. Those cases check for a combination of incorrect parity bits and based on the combination the error produces, the part of the encoded message that has the error can be determined. The statements below shows which erroneous bit leads to which combination of incorrect parity bits:

    - Case 1: incorrect parity bit/s: None → No error
    - Case 2: incorrect parity bit/s: X1 and X2 → error at B1
    - Case 3: incorrect parity bit/s: X1 and X3 → error at B2
    - Case 4: incorrect parity bit/s: X2 and X3 → error at B3
    - Case 5: incorrect parity bit/s: X1 and X2 and X3 → error at B4
    - Case 6: incorrect parity bit/s: X1 → error at X1
    - Case 7: incorrect parity bit/s: X2 → error at X2
    - Case 8: incorrect parity bit/s: X3 → error at X3

  Hamming (7, 4) works on fixed length 4-bit binary strings. Since DNAcodeX uses the Huffman algorithm, the generated sequences can sometimes not be divisible by 4. For this reason, there was the need to come up with different rules to deal with the leftover sequences. We modified Hamming coding and made DNAcodeX go through the sequence adding 3 parity bits for groups of 4 bits checking for any leftover bits at the end of the sequence. After that it checks the length of the leftover
sequence and adds parity bits based on different rules for each length as follows:

- If the number of the leftover bits is 3 (B1, B2, B3), 3 parity bits are added based on the following rules:
    - X1 = B1 ⊕ B2
    - X2 = B2 ⊕ B3
    - X3 = B1 ⊕ B3
        
    We can call it Hamming (6, 3).
  
    Cases would be:
  
      - Case 1 : incorrect parity bit/s: None → No error
      - Case 2: incorrect parity bit/s: X1 and X3 → error at B1
      - Case 3: incorrect parity bit/s: X1 and X2 → error at B2
      - Case 4: incorrect parity bit/s: X2 and X3 → error at B3
      - Case 5: incorrect parity bit/s: X1 → error at X1
      - Case 6: incorrect parity bit/s: X2 → error at X2
      - Case 7: incorrect parity bit/s: X3 → error at X3
- If the number of the leftover bits is 2 (B1, B2), 3 parity bits are also added based on rules that are slightly different:
    - X1 = 1 – B1 (Flipping the bit)
    - X2 = 1 – B2
    - X3 = B1 ⊕ B2
     
    We can call it Hamming (5, 2).
  
    Cases would be:
  
      - Case 1: incorrect parity bit/s: None → No error
      - Case 2: incorrect parity bit/s: X1 and X3 → error at B1
      - Case 3: incorrect parity bit/s: X2 and X3 → error at B2
      - Case 4: incorrect parity bit/s: X1 → error at X1
      - Case 5: incorrect parity bit/s: X2 → error at X2
      - Case 6: incorrect parity bit/s: X3 → error at X3

- Finally, if the number of leftover bits is 1 (B1), 2 parity bits that represent a repetition of B1 are
added:
    - If B1 = 1, X1 = X2 = 1
    - If B1 = 0, X1 = X2 = 0
      
     We can call it Hamming (3, 1).

For this case, if an error occurs somewhere in the 3-bit codeword, the correct B1 would be the bit that is represented the most. For example: If the original message is 1, the bit is repeated twice so that the encoded message becomes 111. Assuming an error occurs in the first bit the
message becomes 011. By checking the first bit, it can be concluded that it does not match the bit that is more frequent which is 1. This information is used to perform the correction.

## Mutations Simulator
The mutations_simulator.py script was written in Python for both simulating Single Base Substitution (SBS) mutations in the DNAcodeX generated sequences and performing the experiment to report its effectiveness. The primary focus of the script is to help assess the efficiency of decoding
mutated sequences. The efficiency testing involves comparing two scenarios:
    - When incorporating the Hamming correction algorithm during decoding.
    - When decoding without Hamming correction algorithm.

The mutations simulator takes three inputs:
1. The input sequence that needs to be tested.
2. The rate at which mutations (Single Base Substitution) are introduced in the sequence.
3. The number of times the simulation should be repeated.

We use the cryptographic hash function MD5 (Message-Digest Algorithm 5) to authenticate the content of files or strings. The script first decodes the sequence without introducing any errors to produce a 128-bit reference value using MD5. After that, mutations are introduced based on the provided mutations rate. Then, the script tries to decode the sequence after attempting to detect and correct the introduced errors and produces MD5 hash value for the mutated sequence to compare it with the one of the unmutated sequence. If the MD5 strings match, the script records the value 1 indicating a perfect match. Otherwise, it records 0 (even if one character was decoded incorrectly). The script iterates over the specified number of runs (as provided in the input), introducing mutations, decoding, comparing, and recording data for each run.

## DNAcodeX User Guide
Both the encoding and the decoding processes have been designed to be user-friendly and accessible to anyone who uses Python and the command line. Here, we provide an example of how to execute both the DNAcodeX encoder and decoder software with different options and inputs.

### Encoding
The output of the encoding process is always two files. The first one is a text file that contains the DNA sequence that represents the encoded data. The second output file is a CSV (Comma Separated Values) file and it would contain metadata about each encoding run. This includes the input file name, a unique ID represented by the date and time of each run, the number of added parity bits, compression ratio (if Huffman coding was used), and the length of the output DNA sequence.
There are two required inputs that are necessary for the execution of the encoder on a data file:
1. The name of the input file the user wants to encode. It should be written in full after the flag -f, otherwise an error would arise.
2. The format of the input file and that would be entered following the -t flag. These are examples of possible format options:
    - TXT for text files.
    - PNG, JPEG, JPG for images
    - GZ for compressed files.

Similarly, there are two inputs that are not crucial for running the encoder. One of them yields different results when used. The function -huffman indicates that the Huffman coding algorithm should be used for encoding the input file. If this flag is not called, data would be encoded by simply mapping the binary data to ATCG bases. The output file name (without the extension) after the function -o. This is not necessary and if not specified, the output DNA sequence would be stored in a file with a default name.
**Examples for running the encoder**

Let us assume we wish to encode the file ”bible.txt,” which is located in the same directory as the encoder code. Additionally, we intend to save the resulting DNA sequence output in a text file named ”bible_encoded”. Here is the corresponding command if we want to use the Huffman compression algorithm:
    python3 DNAcodeX_encoder.py -f bible.txt -t txt -o bible_encoded -huffman
If we do not intend to use Huffman for compressing the data, the command would be:
    python3 DNAcodeX_encoder.py -f bible.txt -t txt -o bible_encoded
It should be noted that the previous command generates a larger sequence than when Huffman
coding is used for encoding large files.

### Decoding
Three output files are always generated after each run of the DNAcodeX decoder program. The first one is the decoded file that contains the original data after retrieval from the DNA sequence. The second one is a CSV file that contains metadata about the decoding process for each run. Lastly, the third file is also a CSV file, which includes all of the sequences that have been corrected for substitution errors if any exists, along with information about their corresponding position in the full sequence.

To run the decoder there are two required inputs that without them, the decoder would not execute:
    1. The name of the input file that contains the DNA sequence to be decoded. This is entered by the user after the function -f with the file extension.
    2. The type (format) of the file that the data would represent after being decoded. It should be entered after using the function -t and the format of the encoded           file should be found in the name of the sequence file before the file extension. This argument is important because if the output data file is not a text file,           the output data would be stored in binary instead of characters for the sake of decoding images and other file formats.
    
- Example 1

If the data file that was encoded using DNAcodeX encoder was an image file with the format PNG and the output sequence file is image_encoded. then the full               sequence file name would be image_encoded_PNG.txt.

- Example 2
  
If the data file that was encoded using DNAcodeX encoder was a text file with the extension (txt) and the output sequence file to be bible_encoded. Then the              full sequence file name would be bible_encoded_text.txt

The other inputs are not necessary to run the decoder. The first one is the output file name, and this can be entered by the user without the format (as this would be added automatically based on the parameter after the function -t). The second optional input is the function -huffman and this should be either used or not without entering anything following it. Although using the -huffman function is optional, it should be noted that it must be compatible with how the DNA sequence was encoded in the first place. For example, if the encoded data was compressed using Huffman algorithm by using the function -huffman when encoding the data, the same function needs to be used during the decoding process. Otherwise, DNAcodeX would not be able to decode the sequence properly.

**Examples for running the decoder**

Let us assume that from the encoding example, we have the file “bible_encoded_text.txt” that contains the DNA sequence we want to decode. And we want the output file name that contains thedecoded data to be “bible_decoded.txt”.
If Huffman coding was used, this needs to be specified for the decoder. The command would be:

    python3 DNAcodeX_decoder.py -f bible_encoded_text.txt -t txt -o bible_decoded -huffman
    
On the other hand, if Huffman coding was not used for encoding, we run the same command with
the flag -huffman removed:

    python3 DNAcodeX_decoder.py -f bible_encoded_text.txt -t txt -o bible_decoded

