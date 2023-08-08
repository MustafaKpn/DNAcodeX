import argparse


######################################### General Functions #########################################
def utf8_bin(u):
    # format as 8-digit binary
    return ''.join([f'{i:08b}' for i in u.encode('utf-8')])

def map_to_dna(binary_string):

    table = binary_string.maketrans('10', 'GC')  # Create a translation table to convert '10' to 'GC'
    binary_string = binary_string.translate(table)  # Apply the translation table to convert the binary representation to the encoded marker

    binary_string = list(binary_string)
    for i in range(1, len(binary_string), 2):
        if binary_string[i] == 'C':
            binary_string[i] = 'T'  # Replace 'C' with 'T'
        if binary_string[i] == 'G':
            binary_string[i] = 'A'  # Replace 'G' with 'A'

    binary_string = ''.join(binary_string)
    return binary_string

#################################### Huffman Encoding Functions ####################################
class node:
    def __init__(self, symbol, frequency, left=None, right=None):
        # symbol
        self.symbol = symbol

        # frequency
        self.frequency = frequency

        # Left node
        self.left = left

        # Right node
        self.right = right
        
def build_frequency_table(data):
    """
    Calculates the frequency of symbols in a given string.

    Args:
        data (str): The input string.

    Returns:
        dict: A dictionary representing the frequency of each symbol.
    """
    
    frequency_table = dict()
    for element in data:
        if frequency_table.get(element) is None:
            frequency_table[element] = 1  # Initialize the frequency of the symbol.
        else:
            frequency_table[element] += 1  # Increment the frequency of the symbol.
    print("* Frequency table has been created.")
    return frequency_table

def build_huffman_tree(frequency_table):
    """
    Builds a Huffman tree based on the frequency table.

    Args:
        frequency_table (dict): A dictionary representing the frequency of each symbol.

    Returns:
        node: The root node of the Huffman tree.
    """
    nodes = []
    for symbol, freq in frequency_table.items():
        nodes.append(node(symbol, freq))  # Create a leaf node for each symbol with its frequency.

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda node: node.frequency)  # Sort the nodes based on their frequency.
        left_node = nodes.pop(0)  # Get the node with the lowest frequency.
        right_node = nodes.pop(0)  # Get the next node with the lowest frequency.
        parent_node = node(None, left_node.frequency + right_node.frequency, left_node, right_node)  # Create a parent node with the combined frequency.
        nodes.append(parent_node)  # Add the parent node back to the list of nodes.
    print("* Huffman tree has been built.")
    return nodes[0]  # Return the root node of the Huffman tree.

def build_huffman_codes(node, code='', huffman_codes=[]):
    """
    Builds Huffman codes for each symbol in the Huffman tree.

    Args:
        node (node): The current node in the Huffman tree.
        code (str): The Huffman code generated so far (default: '').
        huffman_codes (list): A list to store the Huffman codes (default: []).

    Returns:
        None
    """
    if node is None:
        return

    if node.symbol is not None:
        huffman_codes[node.symbol] = code  # Assign the Huffman code to the symbol.

    build_huffman_codes(node.left, code + '0', huffman_codes)  # Traverse the left child with 'C' appended to the code.
    build_huffman_codes(node.right, code + '1', huffman_codes)  # Traverse the right child with 'G' appended to the code.

def huffman_encode(data):
    """
    Encodes the input data using Huffman coding.

    Args:
        data (str): The input string to be encoded.

    Returns:
        tuple: A tuple containing the encoded payload and the Huffman codes.
    """
    frequency_table = build_frequency_table(data)  # Calculate the frequency table.
    
    huffman_tree = build_huffman_tree(frequency_table)  # Build the Huffman tree.
    huffman_codes = dict()
    
    build_huffman_codes(huffman_tree, '', huffman_codes)  # Build Huffman codes for each symbol.
    
    encoded_payload = ''.join([huffman_codes[symbol] for symbol in data])  # Encode the input data using the Huffman codes.

    print("* The payload has been encoded into DNA bases using Huffman coding.")    
    return encoded_payload, huffman_codes

def encode_huffman_instructions(huffman_codes):
    """
    Encodes the given Huffman codes using a specific encoding scheme.

    Arguments:
    - huffman_codes: A dictionary containing the Huffman codes.

    Returns:
    - The encoded instructions as a string.
    """
    codes = ''
    for key, value in huffman_codes.items():
        codes += ',' + key + value  # Concatenate the key and value to form the encoded representation of the Huffman codes

    binary_string = utf8_bin(codes)

    # table = binary_string.maketrans('10', 'GC')  # Create a translation table to convert '10' to 'GC'
    # instructions_encoded = binary_string.translate(table)  # Apply the translation table to convert the binary representation to the encoded instructions
    
    # instructions_encoded = instructions_encoded.replace('CG', 'T')  # Replace 'CG' with 'T'
    # instructions_encoded = instructions_encoded.replace('GC', 'A')  # Replace 'GC' with 'A'
    
    return binary_string

def encode_marker(instructions_string):
    """
    Encodes the instructions length using a specific encoding scheme.

    Arguments:
    - instructions_string: The instructions string.

    Returns:
    - The encoded marker and the length of the instructions as a tuple.
    """
    instructions_len = str(len(instructions_string))  # Get the length of the instructions as a string

    binary_string = ''
    bin_list = [bin(ord(chr)) for chr in instructions_len]  # Convert each character of the instructions length to its ASCII value and then to a binary string

    for binary in bin_list:
        binary = binary.replace('0b', '')
        binary = binary.zfill(8)
        binary_string = binary_string + binary  # Concatenate the binary strings to form the complete binary representation

    return binary_string, instructions_len

def gc_counter(string):
    gc = round((string.count('G') + string.count('C'))/len(string)*100, 3)
    return gc

def read_chrs(file_name):
    """
    Encodes the given data using Huffman coding, marker encoding, and marker length encoding.

    Arguments:
    - data: The input data to encode.

    Returns:
    - The encoded string representing the data.
    """
    with open(file_name, 'r', encoding='utf-8', newline='\r\n') as f:
        read = f.read()

    data = ''
    for chr in read:
        data += chr
        
    if '\r' in data:
        print('File contains carriage character')
    else:
        print("File doesn't contain carriage character")
        
    return data

#################################### Hamming Error Correction Functions ####################################

def bit_switch(bit):
    if bit == 1:
        return 0
    elif bit == 0:
        return 1
    
def add_hamming(string):
    string_list = []

    for i in string:
        string_list.append(int(i))

    parity_list = []
    if len(string_list) == 4:
        x1 = string_list[0] ^ string_list[1] ^ string_list[3]
        parity_list.append(str(x1))
        x2 = string_list[0] ^ string_list[2] ^ string_list[3]
        parity_list.append(str(x2))
        x3 = string_list[1] ^ string_list[2] ^ string_list[3]
        parity_list.append(str(x3))

    elif len(string_list) == 3:
        x1 = string_list[0] ^ string_list[1]
        parity_list.append(str(x1))
        x2 = string_list[1] ^ string_list[2]
        parity_list.append(str(x2))
        x3 = string_list[0] ^ string_list[2]
        parity_list.append(str(x3)) 

    elif len(string_list) == 2:
        x1 = bit_switch(string_list[0])
        parity_list.append(str(x1))
        x2 = bit_switch(string_list[1])
        parity_list.append(str(x2))
        x3 = string_list[0] ^ string_list[1]
        parity_list.append(str(x3))

    elif len(string_list) == 1:
        x1 = string_list[0]
        x2 = string_list[0]
        parity_list.append(str(x1))
        parity_list.append(str(x2))

    binary_string = string + ''.join(parity_list)
    return binary_string

def add_hamming_to_string(string):
    codewords = ''
    parity_counts = 0

    for i in range(0, len(string), 4):
        bits_string = string[i:i+4]
        codewords = codewords + add_hamming(bits_string)

        if len(bits_string) == 4 or len(bits_string) == 3 or len(bits_string) == 2:
            parity_counts += 3
        elif len(bits_string) == 1:
            parity_counts += 2
    
    print('{} parity bits were added.'.format(parity_counts))
    return codewords

def file_to_binary(file_data):
    bytes_list = []
    for byte in file_data:
        binary = str(bin(byte)).replace('0b', '').zfill(8)
        bytes_list.append(binary)

    binary_string = ''.join(bytes_list)
    
    return binary_string

############################################################################################################

parser = argparse.ArgumentParser(description='Huffman DNA encoding system.')

parser.add_argument('-f', '--file_name', required=True, type=str, metavar='', help='The file name you want to encode.')
parser.add_argument('-huffman', '--Huffman', required=False, action='store_true', help='To be called if you want the encoded file to be compressed using Huffman variable length codes.')
parser.add_argument('-t', '--type', required=True, choices=['jpg', 'jpeg', 'png', 'txt', 'gz', 'txt.gz'], metavar='', help='The format of the file you are encoding.')
parser.add_argument('-o', '--output_filename', required=False, type=str, default='encoded_data.txt', metavar='', help='The name of the output file you want to save the encoded data in.')

args = parser.parse_args()

if __name__ == '__main__':

    if args.Huffman == True:
        if args.type == 'txt':
            data = read_chrs(args.file_name)

            suffix = '_text.txt'
            data_bits = len(data) * 8
            

        elif args.type == 'jpeg' or args.type == 'jpg' or args.type == 'png' or args.type == 'gz' or args.type == 'txt.gz':
            with open(args.file_name, 'rb') as f:
                read = f.read()
                
            data = ''
            for byte in read:
                data += str(byte).zfill(3)

            suffix = '_{}.txt'.format(args.type)

        encoded_payload, huffman_codes = huffman_encode(data)  # Perform Huffman encoding on the data to obtain encoded data and Huffman codes
        encoded_instructions = encode_huffman_instructions(huffman_codes)  # Encode the Huffman codes to obtain the encoded instructions
        encoded_marker, len_instructions_len = encode_marker(encoded_instructions)  # Encode the length of the instructions to obtain the marker and length of instructions
        marker_len = encode_marker(len_instructions_len)  # Encode the length of the instructions length to obtain the marker length
        binary_data = marker_len[0] + encoded_marker + encoded_instructions + encoded_payload # Concatenate the marker length, marker, instructions, and data to form the final encoded string
        encoded_payload_bits = len(encoded_payload)

        # print("\n\033[1;34m#################### Encoding Info ####################\033[0m")
        # print("> Huffman compression is applied")
        # print("> Space usage before Huffman encoding: \033[1;31m{}\033[0m bits".format(data_bits))
        # print("> Space usage after Huffman encoding: \033[1;32m{}\033[0m bits".format(encoded_payload_bits))
        # print("> Compression ratio: \033[1;32m{} %\033[0m".format(round((encoded_payload_bits)/data_bits * 100, 3)))
        # print("> GC-content of the file: {} %".format(gc_counter(binary_data)))
        # # print("\n> Full length of the encoded file: \033[1;32m{}\033[0m DNA bases".format((len(dna_mapped_data))))  # Print the length of the encoded string
        # # print("> Ratio of decoding information to the full encoded data: \033[1;32m{} %\033[0m".format(round((len(marker_len) + len(encoded_marker) + len(encoded_instructions))/len(encoded_string)*100, 3)))
            

            
    elif args.Huffman == False:
        if args.type == 'txt':
            with open(args.file_name, 'r', encoding='utf-8', newline='\r\n') as f:
                read = f.read()
            binary_data = utf8_bin(read)  
            suffix = '_text.txt'

        elif args.type == 'jpeg' or args.type == 'jpg' or args.type == 'png' or args.type == 'gz' or args.type == 'txt.gz':
            with open(args.file_name, 'rb') as f:
                read = f.read()
            binary_data = file_to_binary(read)
            suffix = '_{}.txt'.format(args.type)

    binary_data_hamming = add_hamming_to_string(binary_data)
    output_data = map_to_dna(binary_data_hamming)

    output_filename = args.output_filename + suffix
    with open(output_filename, 'w') as f:
        f.write(output_data)
    print("\n> Note: DNA encoded data was saved in the \033[1;36m{}\033[0m".format(output_filename))
    