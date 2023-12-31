from bw_coding import *
from run_length_coding import *

original_data = 'aaabbb893458faaa238755fks;dkjfaf;lkjoillkslkji'
rl_encoded_data = run_length_encode(original_data)
burrows_encoded_data = burrows_wheeler_encode(rl_encoded_data)
burrows_decoded_data = burrows_wheeler_decode(burrows_encoded_data)
decoded_data = run_length_decode(burrows_decoded_data)
print('original_data',original_data)
print('decoded_data',decoded_data)
print('original_data equals encoded? ',original_data == decoded_data)
