from arithmetic import *
import time

# Load the sample text
sample_text = load_file("sample_text_short.txt")
precision = 10
batch_size = 5
num_bits = 16

#----------------------------ENCODING---------------------------#
start_time = time.time()
encoder = ArithmeticEncoder(precision=precision, batch_size=batch_size, num_bits=num_bits) # Create an instance of ArithmeticEncoder
encoder.encode(msg=sample_text)
end_time = time.time()
print(f"Elapsed time for encoding the message: {end_time - start_time} seconds.")

#----------------------------DECODING---------------------------#
# Load the encoded file
encoded_msg_list, msg_len, freq_table_list = load_encoded_msg(msg_path='encoded_msg.ae', helpers_path='decoder_helpers.ae', num_bits=num_bits)

start_time = time.time()
decoder = ArithmeticDecoder(precision=precision) # Create an instance of ArithmeticDecoder
decoded_msg = decoder.decode(encoded_msg_list, msg_len, freq_table_list)

end_time = time.time()
print(f"Elapsed time for decoding the message: {end_time - start_time} seconds.")

# Check to see if decoding worked properly
if sample_text == decoded_msg:
    print("Decoded message matches original message!!")
else:
    print("Decoded message DOES NOT match original message.")
