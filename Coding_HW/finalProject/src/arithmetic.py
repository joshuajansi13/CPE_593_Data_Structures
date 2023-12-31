from typing import Dict, List
from bitarray import bitarray
from decimal import Decimal, getcontext

import pickle 
import bz2


def load_file(file_path: str) -> str:
    '''
    Loads the text file and turns it to a str type. 
    '''
    file = open(file=file_path, mode='r')
    lines = file.readlines()
    file.close()

    input_str = ""

    for line in lines:
        input_str += line

    return input_str

def load_encoded_msg(msg_path: str, helpers_path: str, num_bits: int) -> tuple[bitarray, str, Dict]:
        '''
        Loads the encoded message: encoded message (single decimal value), message length, and probability table.
        '''
        with open(msg_path, 'rb') as file:
            encoded_msg = bitarray()
            encoded_msg.fromfile(file)

        encoded_msg_list = [list(x) for x in (zip(*[iter(encoded_msg.tolist())] * num_bits))]

        with open(helpers_path, 'rb') as file:
            helpers = pickle.load(file)

        msg_len = helpers.pop()

        return encoded_msg_list, msg_len, helpers

class ArithmeticEncoder:
    def __init__(self, precision=10, batch_size=5, num_bits=16) -> None:
        self.encoded_msg_dict = {}
        self.batch_size = batch_size
        self.num_bits = num_bits
        self.encoded_msg = bitarray()
        self.msg_len = ""
        self.freq_table_list = []
        getcontext().prec = precision

    def calc_freq_table(self, msg: str) -> Dict:
        '''
        Calculates the frequency table, given a message (as a string).
        '''
        frequency_table = {}

        for symbol in msg:
            if symbol not in frequency_table.keys():
                frequency_table[symbol] = 1
            else:
                frequency_table[symbol] += 1

        return frequency_table
    
    def calc_prob_table(self, frequency_table: Dict) -> Dict:
        '''
        Calculates the probability table, given the frequency table.
        '''
        probability_table = {} 

        total_frequency = sum(list(frequency_table.values()))
        cum_sum = 0

        for key, value in frequency_table.items():
            probability_table[key] = (cum_sum, cum_sum + value / total_frequency)
            cum_sum += value / total_frequency

        return probability_table

    def encode(self, msg: str) -> None:
        #Break up the message into chunks
        n = self.batch_size
        msg_list = [msg[i:i+n] for i in range(0, len(msg), n)]

        for msg_str in msg_list:
            interval_min = Decimal(0.0)
            interval_max = Decimal(1.0)

            freq_table = self.calc_freq_table(msg_str)
            prob_table = self.calc_prob_table(freq_table)

            self.freq_table_list.append(freq_table)

            # Calculate the sub-interval that the msg_str belongs in
            for symbol in msg_str:
                interval_range = interval_max - interval_min
                interval_max = interval_min + interval_range * Decimal(prob_table[symbol][1])
                interval_min = interval_min + interval_range * Decimal(prob_table[symbol][0])

            # Find binary sequence that is contained within the sub-interval
            counter = 0
            bin_seq = ""
            while interval_max < Decimal(0.5) or interval_min > Decimal(0.5):
                if interval_max < Decimal(0.5):
                    bin_seq += '0'
                    interval_min = Decimal(2.0) * interval_min
                    interval_max = Decimal(2.0) * interval_max
                elif interval_min > Decimal(0.5):
                    bin_seq += '1'
                    interval_min = Decimal(2.0) * (interval_min - Decimal(0.5))
                    interval_max = Decimal(2.0) * (interval_max - Decimal(0.5))

            while interval_min > Decimal(0.25) and interval_max < Decimal(0.75):
                counter += 1
                interval_min = Decimal(2.0) * (interval_min - Decimal(0.25))
                interval_max = Decimal(2.0) * (interval_max - Decimal(0.25))
                
            counter += 1
            if interval_min <= Decimal(0.25):
                bin_seq = bin_seq + '0' + ('1' * counter)
            else:
                bin_seq = bin_seq + '1' + ('0' * counter)                

            bits = bitarray(self.num_bits)
            bits.setall(0)
            bits[0:len(bin_seq)] = bitarray(bin_seq)
            self.encoded_msg_dict[msg_str] = bits

        self.encoded_msg.encode(self.encoded_msg_dict, msg_list)

        # serialize the substring length
        if len(msg_str) != self.batch_size:
            self.msg_len = str(self.batch_size) + ',' + str(len(msg_str))
        else:
            self.msg_len = str(self.batch_size)

        # Add the message length to the end of the frequency table list
        self.freq_table_list.append(self.msg_len)

        with open('encoded_msg.ae', 'wb') as file:
            self.encoded_msg.tofile(file)

        with open("decoder_helpers.ae", 'wb') as file:
            pickle.dump(self.freq_table_list, file)

        with open("decoder_helpers.ae", "rb") as file, bz2.open("compressed.bz2", "wb") as bz:
            bz.writelines(file)


class ArithmeticDecoder:
    def __init__(self, precision=10) -> None:
        self.decoded_msg = ""
        getcontext().prec = precision

    def bin2float(self, bin: List) -> Decimal:
        dec = Decimal(0.0)
        for i in range(1, len(bin)):
            dec += Decimal(bin[i-1] * (2 ** -i))

        return dec
    
    def calc_prob_table(self, frequency_table: Dict) -> Dict:
        '''
        Calculates the probability table, given the frequency table.
        '''
        probability_table = {} 

        total_frequency = sum(list(frequency_table.values()))
        cum_sum = 0

        for key, value in frequency_table.items():
            probability_table[key] = (cum_sum, cum_sum + value / total_frequency)
            cum_sum += value / total_frequency

        return probability_table

    def decode(self, encoded_msg_list: List, msg_len: str, freq_table_list: List) -> str:
        '''
        Decodes the encoded message.
        '''
        if ',' in msg_len:
            msg_len = [int(i) for i in msg_len.split(',')]
        else:
            msg_len = int(msg_len)

        for idx in range(len(encoded_msg_list)):
            encoded_msg = encoded_msg_list[idx]
            prob_table = self.calc_prob_table(freq_table_list[idx])

            if idx == len(encoded_msg_list) - 1 and len(msg_len) > 1:
                message_length = msg_len[-1]
            else:
                message_length = msg_len[0]

            encoded_msg_dec = self.bin2float(encoded_msg)

            interval_min = Decimal(0.0)
            interval_max = Decimal(1.0)
            counter = 0

            for _ in range(message_length):
                for symbol, val in prob_table.items():
                    interval_range = interval_max - interval_min
                    sub_interval_max = interval_min + interval_range * Decimal(val[1])
                    sub_interval_min = interval_min + interval_range * Decimal(val[0])

                    if encoded_msg_dec >= sub_interval_min and encoded_msg_dec < sub_interval_max:
                        self.decoded_msg += symbol
                        interval_min = sub_interval_min
                        interval_max = sub_interval_max
                        counter += 1
                        break
                
        return self.decoded_msg

