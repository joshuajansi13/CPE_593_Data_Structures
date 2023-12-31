# Hash Function Used in Rabin-Karp algorithm

The hash function I used for the pattern was:

hash value of p = Σ(v \* dm-1) % q,

where p = pattern string, v = integer representation of the unicode character, d = 10 (base), m = length of the input text, and q = some prime number (13, in my case).
