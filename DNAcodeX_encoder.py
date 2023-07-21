import argparse

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

    build_huffman_codes(node.left, code + 'C', huffman_codes)  # Traverse the left child with 'C' appended to the code.
    build_huffman_codes(node.right, code + 'G', huffman_codes)  # Traverse the right child with 'G' appended to the code.


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
    
    encoded_payload = list(encoded_payload)
    for i in range(1, len(encoded_payload), 2):
        if encoded_payload[i] == 'C':
            encoded_payload[i] = 'T'  # Replace 'C' with 'T'.
        if encoded_payload[i] == 'G':
            encoded_payload[i] = 'A'  # Replace 'G' with 'A'.
    encoded_payload = ''.join(encoded_payload)
    
    
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

    binary_string = ''
    bin_list = [bin(ord(chr)) for chr in codes]  # Convert each character to its ASCII value and then to a binary string
    
    for binary in bin_list:
        binary = binary.replace('0b', '')
        if len(binary) != 7:
            binary = ('0' * (7 - len(binary))) + binary  # Pad the binary string with leading zeros to ensure it has a length of 7
        binary_string = binary_string + binary  # Concatenate the binary strings to form the complete binary representation

    table = binary_string.maketrans('10', 'GC')  # Create a translation table to convert '10' to 'GC'
    instructions_encoded = binary_string.translate(table)  # Apply the translation table to convert the binary representation to the encoded instructions
    
    instructions_encoded = instructions_encoded.replace('CG', 'T')  # Replace 'CG' with 'T'
    instructions_encoded = instructions_encoded.replace('GC', 'A')  # Replace 'GC' with 'A'
    
    return instructions_encoded


def encode_marker_len(marker):
    """
    Encodes the length of a marker using a specific encoding scheme.

    Arguments:
    - marker: The marker string.

    Returns:
    - The encoded marker length as a string.
    """
    marker_len = str(len(marker))  # Get the length of the marker as a string
    binary = bin(ord(marker_len))  # Convert the length to its ASCII value and then to a binary string

    binary = binary.replace('0b', '')
    if len(binary) != 7:
        binary = ('0' * (7 - len(binary))) + binary  # Pad the binary string with leading zeros to ensure it has a length of 7

    table = binary.maketrans('10', 'GC')  # Create a translation table to convert '10' to 'GC'
    marker_len_encoded = binary.translate(table)  # Apply the translation table to convert the binary representation to the encoded marker length

    marker_len_encoded = list(marker_len_encoded)
    for i in range(1, len(marker_len_encoded), 2):
        if marker_len_encoded[i] == 'C':
            marker_len_encoded[i] = 'T'  # Replace 'C' with 'T'
        if marker_len_encoded[i] == 'G':
            marker_len_encoded[i] = 'A'  # Replace 'G' with 'A'
    marker_len_encoded = ''.join(marker_len_encoded)  # Convert the list back to a string

    return marker_len_encoded


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
        if len(binary) != 7:
            binary = ('0' * (7 - len(binary))) + binary  # Pad the binary string with leading zeros to ensure it has a length of 7
        binary_string = binary_string + binary  # Concatenate the binary strings to form the complete binary representation

    table = binary_string.maketrans('10', 'GC')  # Create a translation table to convert '10' to 'GC'
    marker_encoded = binary_string.translate(table)  # Apply the translation table to convert the binary representation to the encoded marker

    marker_encoded = list(marker_encoded)
    for i in range(1, len(marker_encoded), 2):
        if marker_encoded[i] == 'C':
            marker_encoded[i] = 'T'  # Replace 'C' with 'T'
        if marker_encoded[i] == 'G':
            marker_encoded[i] = 'A'  # Replace 'G' with 'A'

    marker_encoded = ''.join(marker_encoded)  # Convert the list back to a string

    return marker_encoded, instructions_len

def gc_counter(string):
    gc = round((string.count('G') + string.count('C'))/len(string)*100, 3)
    return gc

def HuffGene_encode(file_name, output_filename = 'encoded_data.txt'):
    """
    Encodes the given data using Huffman coding, marker encoding, and marker length encoding.

    Arguments:
    - data: The input data to encode.

    Returns:
    - The encoded string representing the data.
    """
    with open(file_name, 'rb') as f:
        ascii_read = f.read()

    data = ''
    for value in ascii_read:
        data += chr(value)

    encoded_payload, huffman_codes = huffman_encode(data)  # Perform Huffman encoding on the data to obtain encoded data and Huffman codes
    encoded_instructions = encode_huffman_instructions(huffman_codes)  # Encode the Huffman codes to obtain the encoded instructions
    encoded_marker, len_instructions_len = encode_marker(encoded_instructions)  # Encode the length of the instructions to obtain the marker and length of instructions

    marker_len = encode_marker_len(len_instructions_len)  # Encode the length of the instructions length to obtain the marker length
    encoded_string = marker_len + encoded_marker + encoded_instructions + encoded_payload  # Concatenate the marker length, marker, instructions, and data to form the final encoded string
    
    data_bits = len(data) * 8
    encoded_payload_bits = len(encoded_payload)
    
    print("\n\033[1;34m#################### Encoding Info ####################\033[0m")
    print("> Space usage before Huffman encoding: \033[1;31m{}\033[0m bits".format(data_bits))
    print("> Space usage after Huffman encoding: \033[1;32m{}\033[0m bits".format(encoded_payload_bits))
    print("> Compression ratio: \033[1;32m{} %\033[0m".format(round((encoded_payload_bits)/data_bits * 100, 3)))
    
    print("\n> Length of marker: {} DNA bases".format(len(encoded_marker)))
    print("> Length of Huffman dictionary: {} DNA bases".format(len(encoded_instructions)))
    print("> Length of payload: {} DNA bases".format(len(encoded_payload)))
    
    print("\n> GC-content of Huffman dictionary: {} %".format(gc_counter(encoded_instructions)))
    print("> GC-content of payload: {} %".format(gc_counter(encoded_payload)))
    print("> GC-content of the file: {} %".format(gc_counter(encoded_string)))
    
    print("\n> Full length of the encoded file: \033[1;32m{}\033[0m DNA bases".format((len(encoded_string))))  # Print the length of the encoded string
    print("> Ratio of decoding information to the full encoded data: \033[1;32m{} %\033[0m".format(round((len(marker_len) + len(encoded_marker) + len(encoded_instructions))/len(encoded_string)*100, 3)))
    
    with open(output_filename, 'w') as f:
        f.write(encoded_string)
    print("\n> Note: DNA encoded data was saved in the \033[1;36m{}\033[0m".format(output_filename))
    
    return encoded_string

# HuffGene_encode('alice29.txt')
parser = argparse.ArgumentParser(description='Huffman DNA encoding system.')

parser.add_argument('-f', '--file_name', required=True, type=str, metavar='', help='The file name you want to encode.')
parser.add_argument('-t', '--output_filename', required=False, type=str, default='encoded_data.txt', metavar='', help='The name of the output file you want to save the encoded data in.')

args = parser.parse_args()

if __name__ == '__main__':
    HuffGene_encode(args.file_name, args.output_filename)

