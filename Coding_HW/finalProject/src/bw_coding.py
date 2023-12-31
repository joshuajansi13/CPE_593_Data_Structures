def burrows_wheeler_encode(data,add_char='!'):
    lst_of_transforms = []
    data = data + add_char
    for i in range(len(data)):
        lst_of_transforms.append(data[i:] + data[:i])
    lst_of_transforms = sorted(lst_of_transforms)
    bwt_encoded = ''.join(shift[-1] for shift in lst_of_transforms)

    return bwt_encoded

def burrows_wheeler_decode(bwt_string,add_char='!'):
    length_bwt = len(bwt_string)
    sorted_bwt = sorted(bwt_string)
    left_shift = [0] * length_bwt
    start_index = bwt_string.index(add_char)
    
    positions = [[] for _ in range(128)]

    for i, char in enumerate(bwt_string):
        positions[ord(char)].append(i)

    for i in range(length_bwt):
        left_shift[i] = positions[ord(sorted_bwt[i])].pop(0)

    decoded_chars = [''] * length_bwt
    current_index = start_index
    for i in range(length_bwt):
        current_index = left_shift[current_index]
        decoded_chars[length_bwt - 1 - i] = bwt_string[current_index]

    decoded_string = ''.join(decoded_chars)
    return decoded_string[::-1].rstrip(add_char)
