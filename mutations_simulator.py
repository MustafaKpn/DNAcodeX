import argparse
import hashlib
import random
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
        codes = [code for code in codes_list1]

        codes_list2 = codes_list[1].split(',')  # Split the second set of codes
        codes_list2[0] = ',' + codes_list2[0]
        codes = [code for code in codes_list2]
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
    bits = [int(i) for i in string]
    error = False

    if len(bits) == 7:
        parity_indices = [(0, 1, 3), (0, 2, 3), (1, 2, 3)]
        parities = [bits[i] ^ bits[j] ^ bits[k] for i, j, k in parity_indices]

        p1 = parities[0] == bits[4]
        p2 = parities[1] == bits[5]
        p3 = parities[2] == bits[6]

        if p1 == False and p2 == False and p3 == True:
            bits[0] = bit_switch(bits[0])
            error = True

        elif p1 == False and p2 == True and p3 == False:
            bits[1] = bit_switch(bits[1])
            error = True

        elif p1 == True and p2 == False and p3 == False:
            bits[2] = bit_switch(bits[2])
            error = True 

        elif p1 == False and p2 == False and p3 == False:
            bits[3] = bit_switch(bits[3])
            error = True

        elif p1 == False and p2 == True and p3 == True:
            bits[4] = bit_switch(bits[4])
            error = True

        elif p1 == True and p2 == False and p3 == True:
            bits[5] = bit_switch(bits[5])

        elif p1 == True and p2 == True and p3 == False:
            bits[6] = bit_switch(bits[6])
            error = True
    
    elif len(bits) == 6:
        parity_indices = [(0, 1), (1, 2), (0, 2)]
        parities = [bits[i] ^ bits[j] for i, j in parity_indices]

        p1 = parities[0] == bits[3]
        p2 = parities[1] == bits[4]
        p3 = parities[2] == bits[5]

        if p1 == False and p2 == True and p3 == False:
            bits[0] = bit_switch(bits[0])
            error = True

        elif p1 == False and p2 == False and p3 == True:
            bits[1] = bit_switch(bits[1])
            error = True

        elif p1 == False and p2 == False and p3 == True:
            bits[2] = bit_switch(bits[2])
            error = True 

        elif p1 == False and p2 == True and p3 == True:
            bits[3] = bit_switch(bits[3])
            error = True

        elif p1 == True and p2 == False and p3 == True:
            bits[4] = bit_switch(bits[4])
            error = True

        elif p1 == True and p2 == True and p3 == False:
            bits[5] = bit_switch(bits[5])
            error = True

    elif len(bits) == 5:
        x1 = bit_switch(bits[0])
        x2 = bit_switch(bits[1])
        x3 = bits[0] ^ bits[1]

        p1 = x1 == bits[2]
        p2 = x2 == bits[3]
        p3 = x3 == bits[4]

        if p1 == False and p2 == True and p3 == False:
            bits[0] = bit_switch(bits[0])
            error = True

        elif p1 == True and p2 == False and p3 == False:
            bits[1] = bit_switch(bits[1])
            error = True

        elif p1 == False and p2 == True and p3 == True:
            bits[2] = bit_switch(bits[2])
            error = True 

        elif p1 == True and p2 == False and p3 == True:
            bits[3] = bit_switch(bits[3])
            error = True

        elif p1 == True and p2 == True and p3 == False:
            bits[4] = bit_switch(bits[4])
            error = True

    elif len(bits) == 3:
        if bits[0] != max(set(bits), key = bits.count):
            bits[0] = max(set(bits), key = bits.count)
            error = True

    corrected_string = ''.join([str(i) for i in bits])
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
        length = len(binary_string)

        if length == 7:
            data_without_parity += data[i:i+4]
            parity_count += 3
        elif length == 6:
            data_without_parity += data[i:i+3]
            parity_count += 3
        elif length == 5:
            data_without_parity += data[i:i+2]
            parity_count += 3
        elif length == 3:
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

########################## Single Base Substitutions Simulation Functions ##########################

def simulate_substitution(sequence, mutation_rate):
    sequence = list(sequence)
    seq_length = len(sequence)
    num_mutations = int(seq_length * mutation_rate)

    mutation_positions = random.sample(range(seq_length), num_mutations)

    for position in mutation_positions:
        current_nucleotide = sequence[position]
        possible_nucleotides = ['A', 'C', 'G', 'T']
        possible_nucleotides.remove(current_nucleotide)
        new_nucleotide = random.choice(possible_nucleotides)
        sequence[position] = new_nucleotide

    mutated_sequence = ''.join(sequence)
    return mutated_sequence

def run_code(data, huffman, type, output):

    corrected_data = correct_string(data, str(11))[0]
    data_without_parity, parity_count = remove_hamming_bits(corrected_data)

    if huffman == True:
        print("\033[1;32m> Huffman compression is applied\033[0m")
        header_len = decode_header(dna_to_binary(data_without_parity[:8]))  # Decode the marker length from the encoded data string
        instructions_length = decode_header(dna_to_binary(data_without_parity[8: (header_len + 1) * 8]))  # Decode the length of the instructions from the encoded data string
        huffman_instructions_string_binary = utf8_bin_decode(dna_to_binary(data_without_parity[(header_len + 1) * 8: ((header_len + 1) * 8 + instructions_length)]))  # Decode the Huffman instructions from the encoded data string
        huffman_dict = construct_huffman_dict(huffman_instructions_string_binary)  # Construct the Huffman dictionary from the Huffman instructions
        decoded_data = huffman_decode(dna_to_binary(data_without_parity[(header_len + 1) * 8 + instructions_length:]), huffman_dict)  # Decode the data using Huffman decoding
        print("> Huffman compressed data was decoded.")

        if type == 'txt':
            with open(output, 'w', encoding='utf-8') as f:
                f.write(decoded_data)  
                            
    elif type == 'png' or type == 'jpg' or type == 'gz' or type == 'txt.gz':
        with open(output, 'wb') as bytes_file:
            for i in range(0, len(decoded_data), 3):
                integer = int(decoded_data[i:i+3])
                decoded_data = integer.to_bytes(1, byteorder='big')
                bytes_file.write(decoded_data)

    elif huffman == False:
        print("\033[1;31m> Huffman compression is NOT applied\033[0m")
        if type == 'txt':
            decoded_data = utf8_bin_decode(data_without_parity)
            with open(output, 'w') as f:
                f.write(decoded_data)
        
        elif type == 'png' or type == 'jpg' or type == 'gz' or type == 'txt.gz': 
            decoded_data = binary_to_image_bytes(data_without_parity)
            with open(output, 'wb') as binary_file:
                binary_file.write(decoded_data)

    output_file_size = os.path.getsize('./{}'.format(output))

    # if os.path.exists(output):
    #     os.remove(output)
    # else:
    #     pass

    return output_file_size

parser = argparse.ArgumentParser(description='Single Base Substitution Mutations Simulator')

parser.add_argument('-f', '--input_file', required=True, metavar='', type=str, help='The name of the input file you want to run the simulator on.')
parser.add_argument('-m', '--mutations_rate', required=True, metavar='', type=float, help='The rate of the mutations you want to introduce to the sequence')
parser.add_argument('-huffman', '--Huffman', required=False, action='store_true', help='To be called if the input file is compressed using Huffman algorithm.')
parser.add_argument('-t', '--type', required=True, choices=['jpg', 'jpeg', 'png', 'txt', 'gz', 'txt.gz'], metavar='', help='The format of the file you are decoding.')
parser.add_argument('-n', '--n_sims', required=True, type=int, metavar='')
parser.add_argument('-o', '--output_file', required=False, default='data_decoded', type=str)

args = parser.parse_args()
if __name__ == '__main__':

    with open(args.input_file, 'r', encoding='utf-8', newline='\r\n') as f:
        data = f.read()

    output_filename = args.output_file + '.{}'.format(args.type)
    unmutated_file_size = run_code(data, args.Huffman, args.type, output_filename)
    
    number_of_run = 0

    for i in range(0, args.n_sims, 1):
        mutated_data = simulate_substitution(data, args.mutations_rate)
        mutated_output_file_size = run_code(mutated_data, args.Huffman, args.type, output_filename)
        number_of_run += 1
        print('Run: {}'.format(number_of_run))
        retrieval_per = mutated_output_file_size/unmutated_file_size * 100
        if os.path.exists('./Mutations_simulator_report.csv'):
            pass
        else:
            with open('Mutations_simulator_report.csv', 'w') as f:
                f.write('Input File,Run Number,Mutations Rate (%),Data Retrieval Percentage (%)\n')
        
        with open('Mutations_simulator_report.csv', 'a') as f:
            f.write(args.input_file + ',' + str(number_of_run) + ',' + str(args.mutations_rate) + ',' + str(retrieval_per) + '\n')
        
    print("> Final output file size: \033[1;32m{} bytes\033[0m".format(unmutated_file_size))
    print("> Data has been decoded and saved in the file: \033[1;36m{}\033[0m\n".format(output_filename))

else:
    pass