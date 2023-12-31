from bzip2_encode import * 

from collections import defaultdict
import numpy as np
from bitarray import bitarray
import json
import struct
import concurrent.futures
import pickle

files = ['sample_text_short.txt','sample_text.txt','monte_cristo.txt','sample_tiff_img.tiff','sample_cat.jpg']

for file in files:
    prefix = file.split('.')[0]
    data = run_bzip2_compression(file,returned=True)
    decoded_data = run_bzip2_decompression(prefix,returned=True)
    print('Files are equal for', file,': ', data==decoded_data)


