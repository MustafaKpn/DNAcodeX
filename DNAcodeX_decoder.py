import argparse

def decode_marker(marker):
    """
    Decodes the marker using a specific decoding scheme.

    Arguments:
    - marker: The encoded marker string.

    Returns:
    - The decoded marker as an integer.
    """
    table1 = marker.maketrans('TA', 'CG')  # Create a translation table to convert 'TA' to 'CG'
    marker = marker.translate(table1)  # Apply the translation table to convert the marker back to its original form

    table2 = marker.maketrans('GC', '10')  # Create a translation table to convert 'GC' to '10'
    marker = marker.translate(table2)  # Apply the translation table to convert the marker from base-4 to base-2 representation

    integers = ''
    n = 7  # Number of bits in each segment
    x = [marker[i:i+n] for i in range(0, len(marker), n)]  # Split the marker into segments of n bits
    for bit in x:
        bit = int(bit, 2)  # Convert the binary segment to an integer
        bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode()  # Convert the integer to its corresponding ASCII character
        integers += bit  # Concatenate the ASCII characters to form the decoded marker string
    integers = int(integers)  # Convert the decoded marker string to an integer

    return integers

def utf8_bin_decode(string):
    decoded_string = ''
    while len(string) != 0:

        if string.startswith('0'):
            f = string[:8]
            string = string.removeprefix(f)
            bit = int(f, 2)  # Convert the binary segment to an integer
            bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
            decoded_string += bit    

        elif string.startswith('110'):
            f = string[0:16]
            string = string.removeprefix(f)
            bit = int(f, 2)  # Convert the binary segment to an integer
            bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
            decoded_string += bit

        elif string.startswith('1110'):
            f = string[0:24]
            string = string.removeprefix(f)
            bit = int(f, 2)  # Convert the binary segment to an integer
            bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
            decoded_string += bit

        elif string.startswith('11110'):
            f = string[0:32]
            string = string.removeprefix(f)
            bit = int(f, 2)  # Convert the binary segment to an integer
            bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode('utf-8')
            decoded_string += bit
        else:
            break
        
    return decoded_string

def decode_huffman_instructions(instructions_nuc):
    """
    Decodes the Huffman instructions using a specific decoding scheme.

    Arguments:
    - instructions_nuc: The encoded Huffman instructions string.

    Returns:
    - The decoded Huffman instructions as a string.
    """
    instructions_nuc = instructions_nuc.replace('T', 'CG')  # Replace 'T' with 'CG'
    instructions_nuc = instructions_nuc.replace('A', 'GC')  # Replace 'A' with 'GC'
    
    table = instructions_nuc.maketrans('GC', '10')  # Create a translation table to convert 'GC' to '10'
    instructions_bin = instructions_nuc.translate(table)  # Apply the translation table to convert the instructions from base-4 to base-2 representation

    binary_string = utf8_bin_decode(instructions_bin)
    # chrs = ''
    # n = 7  # Number of bits in each segment
    # x = [instructions_bin[i:i+n] for i in range(0, len(instructions_bin), n)]  # Split the instructions into segments of n bits
    # for bit in x:
    #     bit = int(bit, 2)  # Convert the binary segment to an integer
    #     bit = bit.to_bytes((bit.bit_length() + 7) // 8, 'big').decode()  # Convert the integer to its corresponding ASCII character
    #     chrs += bit  # Concatenate the ASCII characters to form the decoded instructions string

    return binary_string

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
    print(inverse_codes)
    print("inverse codes were created")
    table = encoded_data.maketrans('TA', 'CG')  # Create a translation table to convert 'TA' to 'CG'
    encoded_data = encoded_data.translate(table)  # Apply the translation table to convert the encoded data back to its original form
    print('Encoded data was transferred to CG')
    # open(file_name, 'w').close()
    # print('{} was created'.format(file_name))

    for bit in encoded_data:
        current_code += bit
        # print('Checking if code is in Huffman dictionary')
        if current_code in inverse_codes:
            # print('Code was found in the Huffman dictionary')
            # print('Adding the Huffman code to the file')
            decoded_data += inverse_codes[current_code]  # Append the decoded character to the decoded data
            # with open(file_name, 'a') as f:
            #     f.write(inverse_codes[current_code])
            current_code = ''  # Reset the current code
        else:
            # print('code passed')
            continue
    return decoded_data

def DNAcodeX_decode(file_name, output_filename='data_decoded.txt'):
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

    marker_len = decode_marker(encoded_data[:7])  # Decode the marker length from the encoded data string
    print('Marker has been decoded')

    instructions_length = decode_marker(encoded_data[7: (marker_len + 1) * 7])  # Decode the length of the instructions from the encoded data string
    print('Instructions length is {}'.format(instructions_length))

    huffman_instructions_string = decode_huffman_instructions(encoded_data[(marker_len + 1) * 7: ((marker_len + 1) * 7 + instructions_length)])  # Decode the Huffman instructions from the encoded data string
    print('Huffman dictionary has been decoded.')
    huffman_dict = construct_huffman_dict(huffman_instructions_string)  # Construct the Huffman dictionary from the Huffman instructions
    print('Huffman dictionary has been constructed')
    data_decoded = huffman_decode(encoded_data[(marker_len + 1) * 7 + instructions_length:], huffman_dict)  # Decode the data using Huffman decoding
    print('Data has been decoded')

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(data_decoded)
    print("Data has been decoded and saved in the file: {}".format(output_filename))
    # return data_decoded


parser = argparse.ArgumentParser(description='Huffman DNA decoder')

parser.add_argument('-f', '--file_name',required=True, type=str, metavar='', help='The name of the file you want to decode.')
parser.add_argument('-t', '--output_filename', required=True, default='decoded_data.txt', type=str, metavar='', help='The name of the output file you want to save the decoded data in.')

args = parser.parse_args()

if __name__ == '__main__':
    DNAcodeX_decode(args.file_name, args.output_filename)