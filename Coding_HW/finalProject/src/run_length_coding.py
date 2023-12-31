def run_length_encode(data):
    encoded_data = ""
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data += str(count) + '*' + data[i - 1]
            count = 1

    encoded_data += str(count) + '*' + data[-1]

    return encoded_data


def run_length_decode(encoded_data):
    decoded_data = ""
    for i in range(len(encoded_data)):
        if i==0:
            count_str = encoded_data[i]
        elif encoded_data[i].isdigit() and encoded_data[i-1] != '*':
            count_str += encoded_data[i]
        elif encoded_data[i] == '*':
            decoded_data += str(int(count_str)*encoded_data[i+1])
            count_str = ''
            if i==len(encoded_data)-1:
                break

    
