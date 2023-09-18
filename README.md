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
    
        - Since Gs and Cs are converted to As and Ts respectively, errors that substitute A bases with G bases or T bases with C bases are not actually considered errors as they represent the same bit when the                sequence is converted to binary. This mapping method adds up to the robustness of DNAcodeX when correcting single base substitution errors.
    
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
