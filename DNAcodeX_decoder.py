import argparse
import datetime
import os

######################################### General Functions #######################################

def dna_to_binary(data):
    data = data.replace('T', 'C')
    data = data.replace('A', 'G')

    table = data.maketrans('GC', '10')
    decoded_dna = data.translate(table)

    return decoded_dna

def utf8_bin_decode(string):
    decoded_string = ''
    while len(string) != 0:

        if string.startswith('0'):
            f = string[:8]
            string = string.removeprefix(f)
            try:
                bit = int(f, 2)  # Convert the binary segment to an integer
                bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
                decoded_string += bit 
            except:
                pass    

        elif string.startswith('110'):
            f = string[0:16]
            string = string.removeprefix(f)
            try:
                bit = int(f, 2)  # Convert the binary segment to an integer
                bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
                decoded_string += bit
            except:
                pass

        elif string.startswith('1110'):
            f = string[0:24]
            string = string.removeprefix(f)
            try:
                bit = int(f, 2)  # Convert the binary segment to an integer
                bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
                decoded_string += bit
            except:
                pass

        elif string.startswith('11110'):
            f = string[0:32]
            string = string.removeprefix(f)
            try:
                bit = int(f, 2)  # Convert the binary segment to an integer
                bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
                decoded_string += bit
            except:
                pass
        else:
            break
        
    return decoded_string

#################################### Huffman Decoding Functions ####################################

def decode_header(header):
    """
    Decodes the header using a specific decoding scheme.

    Arguments:
    - header: The encoded header string.

    Returns:
    - The decoded header as an integer.
    """
    integers = ''
    n = 8  # Number of bits in each segment
    x = [header[i:i+n] for i in range(0, len(header), n)]  # Split the header into segments of n bits
    for bit in x:
        bit = int(bit, 2)  # Convert the binary segment to an integer
        bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode()  # Convert the integer to its corresponding ASCII character
        integers += bit  # Concatenate the ASCII characters to form the decoded header string
    integers = int(integers)  # Convert the decoded header string to an integer

    return integers

def construct_huffman_dict(instructions_string):
    """
    Constructs a Huffman dictionary from the encoded instructions string.

    Arguments:
    - instructions_string: The encoded instructions string.

    Returns:
    - The Huffman dictionary containing the codes.
    """
    codes = []
    codes_list = []
    huffman_instructions_dict = {}

    if instructions_string.find(',,') != -1:  # Check if multiple sets of codes are present
        codes_list = instructions_string.split(',,')  # Split the instructions into separate code sets
        codes_list1 = codes_list[0].split(',')  # Split the first set of codes
        for code in codes_list1:
            codes.append(code)

        codes_list2 = codes_list[1].split(',')  # Split the second set of codes
        codes_list2[0] = ',' + codes_list2[0]
        for code in codes_list2:
            codes.append(code)
    else:
        codes = instructions_string[1:].split(',')  # Split the codes if only one set is present

    for code in codes:
        if len(code) != 0:
            huffman_instructions_dict[code[0]] = code[1:]  # Create key-value pairs in the dictionary with character as the key and code as the value

    return huffman_instructions_dict

def huffman_decode(encoded_data, huffman_codes):
    """
    Decodes the encoded data using Huffman decoding.

    Arguments:
    - encoded_data: The encoded data to be decoded.
    - huffman_codes: The Huffman codes used for decoding.

    Returns:
    - The decoded data as a string.
    """
    inverse_codes = {value: key for key, value in huffman_codes.items()}  # Create a dictionary of inverse codes (codes as keys and characters as values)
    current_code = ''  # Initialize an empty string to store the current code being processed
    decoded_data = ''  # Initialize an empty string to store the decoded data

    for bit in encoded_data:
        current_code += bit
        if current_code in inverse_codes:
            decoded_data += inverse_codes[current_code]  # Append the decoded character to the decoded data
            current_code = ''  # Reset the current code
        else:
            continue

    return decoded_data

def read_file(file_name):
    """
    Decodes the DNA encoded data in the given file using Huffman coding.
    HuffGen decodes the first 7 DNA bases (first marker) to get the number of digits of the Huffman dictionary length (second marker).
    Then, after decoding the length of the encoded dictionary, it decodes the dictionary and uses the Huffman codes
    found in the dictionary to decode the encoded text.
    The decoding of the first marker, the second marker and Huffman dictionary is based on the fixed length ASCII codes.
    While the encoded data is mapped by the variable length Huffman codes.

    Arguments:
    - file_name: The file name that contains the encoded data in nucleotides.
    - output_filename: The name of the desired output file. (default: data_decoded.txt)

    Returns:
    - The decoded data saved in a text file.

    """
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    encoded_data = ''

    for line in lines:
        encoded_data += line

    return encoded_data

#################################### Hamming Error Correction Functions ############################

def bit_switch(bit):
    if bit == 1:
        return 0
    elif bit == 0:
        return 1
    
def hamming_correct(string):
    test = []
    for i in string:
        test.append(int(i))

    if len(test) == 7:
        x1 = test[0] ^ test[1] ^ test[3]
        x2 = test[0] ^ test[2] ^ test[3]
        x3 = test[1] ^ test[2] ^ test[3]

        p1 = x1 == test[4]
        p2 = x2 == test[5]
        p3 = x3 == test[6]

        error = False

        if p1 == False and p2 == False and p3 == True:
            test[0] = bit_switch(test[0])
            error = True

        elif p1 == False and p2 == True and p3 == False:
            test[1] = bit_switch(test[1])
            error = True

        elif p1 == True and p2 == False and p3 == False:
            test[2] = bit_switch(test[2])
            error = True 

        elif p1 == False and p2 == False and p3 == False:
            test[3] = bit_switch(test[3])
            error = True

        elif p1 == False and p2 == True and p3 == True:
            test[4] = bit_switch(test[4])
            error = True

        elif p1 == True and p2 == False and p3 == True:
            test[5] = bit_switch(test[5])

        elif p1 == True and p2 == True and p3 == False:
            test[6] = bit_switch(test[6])
            error = True

        elif p1 == True and p2 == True and p3 == True:
            error = False
            pass
    
    elif len(test) == 6:
        x1 = test[0] ^ test[1]
        x2 = test[1] ^ test[2]
        x3 = test[0] ^ test[2]

        p1 = x1 == test[3]
        p2 = x2 == test[4]
        p3 = x3 == test[5]

        if p1 == False and p2 == True and p3 == False:
            test[0] = bit_switch(test[0])
            error = True

        elif p1 == False and p2 == False and p3 == True:
            test[1] = bit_switch(test[1])
            error = True

        elif p1 == False and p2 == False and p3 == True:
            test[2] = bit_switch(test[2])
            error = True 

        elif p1 == False and p2 == True and p3 == True:
            test[3] = bit_switch(test[3])
            error = True

        elif p1 == True and p2 == False and p3 == True:
            test[4] = bit_switch(test[4])
            error = True

        elif p1 == True and p2 == True and p3 == False:
            test[5] = bit_switch(test[5])
            error = True

        elif p1 == True and p2 == True and p3 == True:
            error = False
            pass

    elif len(test) == 5:
        x1 = bit_switch(test[0])
        x2 = bit_switch(test[1])
        x3 = test[0] ^ test[1]

        p1 = x1 == test[2]
        p2 = x2 == test[3]
        p3 = x3 == test[4]

        if p1 == False and p2 == True and p3 == False:
            test[0] = bit_switch(test[0])
            error = True

        elif p1 == True and p2 == False and p3 == False:
            test[1] = bit_switch(test[1])
            error = True

        elif p1 == False and p2 == True and p3 == True:
            test[2] = bit_switch(test[2])
            error = True 

        elif p1 == True and p2 == False and p3 == True:
            test[3] = bit_switch(test[3])
            error = True

        elif p1 == True and p2 == True and p3 == False:
            test[4] = bit_switch(test[4])
            error = True

        elif p1 == True and p2 == True and p3 == True:
            error = False
            pass

    elif len(test) == 3:
        if test[0] != max(set(test), key = test.count):
            test[0] = max(set(test), key = test.count)
            error = True
        else:
            error = False
            pass

    corrected_string = ''.join([str(i) for i in test])
    
    return corrected_string, error

def correct_string(string, formatted_time):

    corrected_string = ''
    errors_count = 0

    sequences_file_name = 'DNAcodeX_corrected_seqs_{}.csv'.format(formatted_time)
    open(sequences_file_name, 'w').close()
    
    for i in range(0, len(string), 7):
        codeword_dna = string[i:i+7]
        codeword_binary = dna_to_binary(codeword_dna)
        corrected_codeword_binary, error = hamming_correct(codeword_binary)
        corrected_string += corrected_codeword_binary

        if error == True:
            errors_count += 1
            with open(sequences_file_name, 'a') as f:
                f.write(codeword_dna + ',' + corrected_codeword_binary + ',' + codeword_binary + ',' + '{}:{}\n'.format(i, i+(len(codeword_binary))))

    return corrected_string, errors_count, sequences_file_name

def remove_hamming_bits(data):

    data_without_parity = ''
    parity_count = 0

    for i in range(0, len(data), 7):
        binary_string = data[i:i+7]
        if len(binary_string) == 7:
            data_without_parity += data[i:i+4]
            parity_count += 3
        elif len(binary_string) == 6:
            data_without_parity += data[i:i+3]
            parity_count += 3
        elif len(binary_string) == 5:
            data_without_parity += data[i:i+2]
            parity_count += 3
        elif len(binary_string) == 3:
            data_without_parity += data[i:i+1]
            parity_count += 2
            

    return data_without_parity, parity_count

def binary_to_image_bytes(binary_data):
    image_bytes = b''
    for i in range(0, len(binary_data), 8):
        eight_bits = binary_data[i:i+8]
        integer = int(eight_bits, 2)
        bytes = integer.to_bytes(1, byteorder='big')
        image_bytes += bytes
    
    return image_bytes

#####################################################################################################

parser = argparse.ArgumentParser(description='Huffman DNA decoder')

parser.add_argument('-f', '--file_name',required=True, type=str, metavar='', help='The name of the file you want to decode.')
parser.add_argument('-huffman', '--Huffman', required=False, action='store_true', help='To be called if Huffman compression was used when the file was encoded.')
parser.add_argument('-t', '--type', required=True, choices=['jpg', 'jpeg', 'png', 'txt', 'gz', 'txt.gz'], metavar='', help='The format of the file you are decoding.')
parser.add_argument('-o', '--output_filename', required=True, default='decoded_data.txt', type=str, metavar='', help='The name of the output file you want to save the decoded data in.')

args = parser.parse_args()

if __name__ == '__main__':
    with open(args.file_name, 'r', encoding='utf-8', newline='\r\n') as f:
        data = f.read()

    input_file_size = os.path.getsize('./{}'.format(args.file_name))
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y%m%d%H%M%S")

    print("\n\033[1;34m############################ Decoding Info ############################\033[0m")
    print("\033[1;35m# Input File Name:\033[0m \033[93m{}\033[0m".format(args.file_name))
    print("\033[1;35m# Input Sequence Length:\033[0m \033[93m{} DNA bases\033[0m".format(len(data)))
    print("\033[1;35m# Output File Format:\033[0m \033[93m{}\033[0m".format(args.type))
    print("\033[1;35m# Huffman:\033[0m \033[93m{}\033[0m".format(args.Huffman))
    print("\033[1;35m# Error Correction Method:\033[0m \033[93mHamming\033[0m")

    corrected_data, errors_count, sequences_file_name = correct_string(data, formatted_time)
    print("\n> Hamming correction was applied.")
    print("> Number of errors detected and corrected: \033[1;31m{}\033[0m".format(errors_count))
    print("> The mutated and corrected sequences (if any), were saved in the file: \033[1;36m{}\033[0m".format(sequences_file_name))
    data_without_parity, parity_count = remove_hamming_bits(corrected_data)
    print("> Hamming correction parity check bits were removed from the input file.")
    print("> Number of the removed parity check bits: \033[1;32m{} bits\033[0m".format(parity_count))
    print("> The sequence length after the removal of Hamming parity check bits: \033[1;32m{} DNA bases\033[0m".format(len(data_without_parity)))
    output_filename = args.output_filename + '.{}'.format(args.type)
    open(output_filename, 'w').close()

    if args.Huffman == True:
        print("\033[1;32m> Huffman compression is applied\033[0m")
        header_len = decode_header(dna_to_binary(data_without_parity[:8]))  # Decode the marker length from the encoded data string
        instructions_length = decode_header(dna_to_binary(data_without_parity[8: (header_len + 1) * 8]))  # Decode the length of the instructions from the encoded data string
        huffman_instructions_string_binary = utf8_bin_decode(dna_to_binary(data_without_parity[(header_len + 1) * 8: ((header_len + 1) * 8 + instructions_length)]))  # Decode the Huffman instructions from the encoded data string
        huffman_dict = construct_huffman_dict(huffman_instructions_string_binary)  # Construct the Huffman dictionary from the Huffman instructions
        payload_decoded = huffman_decode(dna_to_binary(data_without_parity[(header_len + 1) * 8 + instructions_length:]), huffman_dict)  # Decode the data using Huffman decoding
        print("> Huffman compressed data was decoded.")

        if args.type == 'txt':
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(payload_decoded)

        elif args.type == 'png' or args.type == 'jpg' or args.type == 'gz' or args.type == 'txt.gz':
            with open(output_filename, 'wb') as bytes_file:
                for i in range(0, len(payload_decoded), 3):
                    integer = int(payload_decoded[i:i+3])
                    bytes_data = integer.to_bytes(1, byteorder='big')
                    bytes_file.write(bytes_data)

    
    elif args.Huffman == False:
        print("\033[1;31m> Huffman compression is NOT applied\033[0m")
        if args.type == 'txt':
            decoded_data = utf8_bin_decode(data_without_parity)
            with open(output_filename, 'w') as f:
                f.write(decoded_data)
        
        elif args.type == 'png' or args.type == 'jpg' or args.type == 'gz' or args.type == 'txt.gz': 
            decoded_data = binary_to_image_bytes(data_without_parity)
            with open(output_filename, 'wb') as binary_file:
                binary_file.write(decoded_data)

    output_file_size = os.path.getsize('./{}'.format(output_filename))
    
    if os.path.exists('./DNAcodeX_decoding_INFO.csv'):
        pass
    else:
        with open('DNAcodeX_decoding_INFO.csv', 'w') as f:
            f.write('Input File,ID(DateTime),Errors Count,Length of Input Sequence,Removed Parity Bits,Length of Sequence After Parity Bits Removal,Output File Size (bytes)\n')
    
    with open('DNAcodeX_decoding_INFO.csv', 'a') as f:
        f.write(args.file_name + ',' + formatted_time + ',' + str(errors_count) + ',' + str(len(data)) + ',' + str(parity_count) + ',' + str(len(data_without_parity)) + ',' + str(output_file_size) + '\n')
    
    print("> Final output file size: \033[1;32m{} bytes\033[0m".format(output_file_size))
    print("> Data has been decoded and saved in the file: \033[1;36m{}\033[0m\n".format(output_filename))