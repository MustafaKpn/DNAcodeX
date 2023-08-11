from DNAcodeX_decoder_copy import *
import random
import argparse


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