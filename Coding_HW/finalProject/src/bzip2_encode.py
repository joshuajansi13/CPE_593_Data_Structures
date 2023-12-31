
from collections import defaultdict
import numpy as np
from bitarray import bitarray
import json
import struct
import concurrent.futures
import pickle
import os

def run_length_encode(data,begin_char = '\x04',end_char = '\x05'):
    encoded_data = ""
    count = 1

    for i in range(1, len(data)):

        if data[i] == data[i - 1]:
            count += 1
        elif count > 5:
            encoded_data +=  4*data[i-1] + begin_char + str(count-4) + end_char
            count = 1
        else:
            encoded_data += count*data[i-1]
            count = 1
    if count > 4:
        encoded_data += 4*data[-1] + begin_char + str(count-4) + end_char
    else:
        encoded_data += count*data[-1]
            
    return encoded_data


def run_length_decode(encoded_data,begin_char = '\x04',end_char = '\x05'):
    decoded_data = ""
    count_str = ''
    is_num = False
    for i in range(len(encoded_data)):
        if i==0:
            decoded_data = encoded_data[i]
        elif encoded_data[i]==begin_char:
            is_num = True
        elif is_num and encoded_data[i] != end_char:
            count_str += encoded_data[i]
        elif encoded_data[i] == end_char:
            decoded_data += str((int(count_str))*encoded_data[i-len(count_str)-2])
            count_str = ''
            is_num=False
        else:
            decoded_data += encoded_data[i]

    return decoded_data

def generate_rotation_matrix(text):
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    return rotations

def burrows_wheeler_encode(data):
    rotations = generate_rotation_matrix(data)
    rotations.sort()
    bwt_result = bytes(rotation[-1] for rotation in rotations)
    original_index = rotations.index(data)
    
    return bwt_result, original_index

def burrows_wheeler_decode(bwt, original_index):
    result = bytearray(len(bwt))
    sorted_bwt = sorted(bwt)
    sorted_occurrences = [0] * 256
    bwt_occurrences = [0] * 256
    sorted_lst = []
    bwt_index = {}

    for i in range(len(bwt)):
        sorted_val = sorted_bwt[i]
        sorted_occurrences[sorted_val] += 1
        sorted_lst.append((sorted_val, sorted_occurrences[sorted_val]))
        bwt_i = bwt[i]
        bwt_occurrences[bwt_i] += 1
        bwt_index[(bwt_i, bwt_occurrences[bwt_i])] = i

    for _ in range(len(bwt)):
        new_val = sorted_lst[original_index]
        result[_] = new_val[0]
        original_index = bwt_index[new_val]

    return bytes(result)


def mtf_encode(data):
    alphabet = bytearray(range(256))
    encoded_data = bytearray()
    for symbol in data:
        index = alphabet.index(symbol)
        encoded_data.append(index)
        alphabet.pop(index)
        alphabet.insert(0, symbol)
    return encoded_data

def mtf_decode(encoded_data):
    alphabet = bytearray(range(256))
    decoded_data = bytearray()
    for index in encoded_data:
        symbol = alphabet[index]
        decoded_data.append(symbol)
        alphabet.remove(symbol)
        alphabet.insert(0, symbol)
    return bytes(decoded_data)



def run_length_encode2(data):
    encoded_data = bytearray()
    count = 0

    for symbol in data:
        if symbol == 0:
            count += 1
        else:
            while count > 255:
                encoded_data.extend([0, 255])
                count -= 255
            if count > 0:
                encoded_data.extend([0, count])
                count = 0
            encoded_data.append(symbol)

    while count > 255:
        encoded_data.extend([0, 255])
        count -= 255

    if count > 0:
        encoded_data.extend([0, count])

    return encoded_data

def run_length_decode2(encoded_data):
    decoded_data = bytearray()

    i = 0
    while i < len(encoded_data):
        symbol = encoded_data[i]
        if symbol == 0:
            count = encoded_data[i + 1]
            decoded_data.extend([0] * count)
            i += 2
        else:
            decoded_data.append(symbol)
            i += 1

    return decoded_data




class Node:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

def build_huffman_tree(frequency_dict):
    nodes = [Node(symbol=s, frequency=f) for s, f in frequency_dict.items()]
    
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.frequency)
        left, right = nodes.pop(0), nodes.pop(0)
        internal_node = Node(frequency=left.frequency + right.frequency, left=left, right=right)
        nodes.insert(0, internal_node)

    return nodes[0]

def build_encoding_dict(node, code="", encoding_dict=None):
    if encoding_dict is None:
        encoding_dict = {}

    if node.symbol is not None:
        encoding_dict[node.symbol] = bitarray(code)
    if node.left:
        build_encoding_dict(node.left, code + '0', encoding_dict)
    if node.right:
        build_encoding_dict(node.right, code + '1', encoding_dict)

    return encoding_dict

def huffman_encode(text):
    frequency_dict = {}
    for symbol in set(text):
        frequency_dict[symbol] = text.count(symbol)
    huffman_tree = build_huffman_tree(frequency_dict)
    encoding_dict = build_encoding_dict(huffman_tree)

    encoded_text = bitarray()
    encoded_text.encode(encoding_dict, text)

    return encoded_text, encoding_dict


def huffman_decode(encoded_text, encoding_dict):
    decoded_text = bytearray()
    current_code = bitarray()

    for bit in encoded_text:
        current_code.append(bit)
        for symbol, code in encoding_dict.items():
            if code == current_code:
                decoded_text.append(symbol)
                current_code = bitarray()  
                break

    return decoded_text


def calculate_bits(encoded_text, encoding_dict):
    encoding_dict_bits = sum(len(code) for code in encoding_dict.values())
    return len(encoded_text) + encoding_dict_bits


def split_into_blocks(data, block_size_kb):
    block_size_bytes = block_size_kb * 1024
    num_blocks = (len(data) + block_size_bytes - 1) // block_size_bytes
    blocks = [data[i * block_size_bytes:(i + 1) * block_size_bytes] for i in range(num_blocks)]    
    return blocks

def concatenate_blocks(blocks):
    sorted_list = sorted(blocks)
    concatenated_result = ''.join([block[1] for block in sorted_list])
    return concatenated_result



def read_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        
    return data

def parallel_processing(items):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_compression, items))

    return results

def concatenate_bytearrays(bytearrays_list):
    result = bytearray()
    for array in bytearrays_list:
        result += array  
    return result

import os

def run_clean_up(file_name):
    file_split = file_name.split('.')
    file_suffix = file_split[1]
    file_prefix = file_split[0]

    try:
        os.remove(file_prefix + '_huff_dcts.pkl')
        print(f"{file_prefix}_huff_dcts.pkl deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_huff_dcts.pkl not found. No file deleted.")

    try:
        os.remove(file_prefix + '_indices.pkl')
        print(f"{file_prefix}_indices.pkl deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_indices.pkl not found. No file deleted.")

    try:
        os.remove(file_prefix + '_file.bin')
        print(f"{file_prefix}_file.bin deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_file.bin not found. No file deleted.")

    try:
        os.remove(file_prefix + '_bw_indices.pkl')
        print(f"{file_prefix}_bw_indices.pkl deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_bw_indices.pkl not found. No file deleted.")

    try:
        os.remove(file_prefix + '_file_header.pkl')
        print(f"{file_prefix}_file_header.pkl deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_file_header.pkl not found. No file deleted.")

    try:
        os.remove(file_prefix + '_decoded.' + file_suffix)
        print(f"{file_prefix}_decoded{file_suffix} deleted.")
    except FileNotFoundError:
        print(f"Error: {file_prefix}_decoded{file_suffix} not found. No file deleted.")



def run_bzip2_compression(file_path,block_size_kb=10,img=False,returned=False):
    huff_dcts = []
    indices = []
    dict_data = []
    bw_indices = []
    data = read_file(file_path)
    data1 = data
    file_split = file_path.split('.')
    filename = file_split[0]
    pickle.dump(file_split, open(filename + '_file_header.pkl','wb'))
    data = bytearray(data)
    blocks = split_into_blocks(data, block_size_kb)
    for i,block in enumerate(blocks):
        burrows_wheeler_encoded,original_rotation_index = burrows_wheeler_encode(block)
        bw_indices.append(original_rotation_index)
        mtf_encoded_result = mtf_encode(burrows_wheeler_encoded)
        run_length_encoded2 = run_length_encode2(mtf_encoded_result)
        huffman_encoded_result, huffman_dict = huffman_encode(run_length_encoded2)
        huff_dcts.append(huffman_dict)
        if i==0:
            block_data = huffman_encoded_result
            ind_val = len(huffman_encoded_result)
            indices.append(ind_val)
            huff_save = huffman_encoded_result
        else:
            block_data += huffman_encoded_result
            ind_val = len(huffman_encoded_result)
            indices.append(ind_val)
        tot_bits = calculate_bits(huffman_encoded_result, huffman_dict)


    
    with open(filename + '_file.bin', 'wb') as binary_file:
        block_data.tofile(binary_file)

    with open(filename + '_huff_dcts.pkl', 'wb') as binary_file:
        pickle.dump(huff_dcts, binary_file)

    with open(filename + '_indices.pkl', 'wb') as binary_file:
        pickle.dump(indices,binary_file)

    with open(filename + '_bw_indices.pkl', 'wb') as binary_file:
        pickle.dump(bw_indices,binary_file)

    if returned:    
        return data1
    return


def run_bzip2_decompression(filename='test_file',returned=False):

    with open(filename + '_huff_dcts.pkl', 'rb') as binary_file:
        huff_dcts = pickle.load(binary_file)

    with open(filename + '_indices.pkl', 'rb') as binary_file:
        indices_lst = pickle.load(binary_file)

    blocks = bitarray()
    with open(filename + '_file.bin', 'rb') as binary_file:
        blocks.fromfile(binary_file)

    with open(filename + '_bw_indices.pkl', 'rb') as binary_file:
        bw_indices = pickle.load(binary_file)
        
    with open(filename + '_file_header.pkl', 'rb') as binary_file:
        file_header = pickle.load(binary_file)
        file_extension = file_header[1]
        file_prefix = file_header[0]

    out_lst = []
    for i, bw_ind in enumerate(bw_indices):
        block = blocks[:indices_lst[i]]
        del blocks[:indices_lst[i]]
        huffman_decoded_result = huffman_decode(block, huff_dcts[i])
        run_length_decoded2 = run_length_decode2(huffman_decoded_result)
        mtf_decoded = mtf_decode(run_length_decoded2)
        bw_decoded = burrows_wheeler_decode(mtf_decoded,bw_ind)
        out_lst.append(bw_decoded)
    fin_out = bytes(concatenate_bytearrays(out_lst))
    with open(file_prefix  + '_decoded.' + file_extension, 'wb') as file:
        file.write(fin_out)



    if returned:
        return fin_out
    return
