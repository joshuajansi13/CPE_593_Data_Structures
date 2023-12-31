import argparse
import inspect
import re
import time
from collections.abc import Callable
from pathlib import Path
from typing import BinaryIO, ParamSpec, TextIO, TypeVar, cast

from arithmetic import ArithmeticDecoder, ArithmeticEncoder, load_encoded_msg
from bzip2_encode import run_bzip2_compression, run_bzip2_decompression
from huffman import BasicHuffmanEncoder, HuffmanDecoder, HybridHuffmanEncoder

P = ParamSpec("P")
T = TypeVar("T")


def time_it(
    function: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    stack = inspect.stack()
    prev_stack = stack[1]
    prev_function_line = prev_stack.lineno
    start_time = time.time()
    ret = function(*args, **kwargs)
    end_time = time.time()
    print(
        f"Elapsed time for {function.__name__} at line {prev_function_line}"
        f": {end_time - start_time} seconds.",
    )
    return ret


def arithmetic_test(text: str) -> None:
    precision = 10
    batch_size = 5
    num_bits = 16

    # ----------------------------ENCODING---------------------------#
    encoder = ArithmeticEncoder(
        precision=precision,
        batch_size=batch_size,
        num_bits=num_bits,
    )
    time_it(encoder.encode, msg=text)

    # ----------------------------DECODING---------------------------#
    # Load the encoded file
    encoded_msg_list, msg_len, freq_table_list = load_encoded_msg(
        msg_path="encoded_msg.ae",
        helpers_path="decoder_helpers.ae",
        num_bits=num_bits,
    )

    decoder = ArithmeticDecoder(precision=precision)

    decoded_msg = time_it(decoder.decode, encoded_msg_list, msg_len, freq_table_list)

    if text == decoded_msg:
        print("Arithmetic: Decoded message matches original message")
    else:
        print("Arithmetic: Decoded message DOES NOT match original message.")
    print()


def bzip2_test(text: str, filename: Path) -> None:
    # encoding
    time_it(run_bzip2_compression, str(filename))
    # decoding
    decoded_msg = cast(bytes, time_it(run_bzip2_decompression, filename.stem))
    # check that input and output are the same
    if Path(filename).read_bytes() == decoded_msg:
        print("Bzip2: Decoded message matches original message!!")
    else:
        print("Bzip2: Decoded message DOES NOT match original message.")
    print()


def _basic_huff_encode(
    code_output: Path,
    data_output: Path,
    data: str | list[str],
) -> None:
    encoder = BasicHuffmanEncoder(data)
    with code_output.open("w") as code_file, data_output.open("wb") as data_file:
        encoder.serialize_code(code_file)
        encoder.serialize_data(data_file)


def _top_n_huff_encode(
    code_output: Path,
    data_output: Path,
    data: list[str],
    n: int,
) -> None:
    encoder = HybridHuffmanEncoder(data, n)
    with code_output.open("w") as code_file, data_output.open("wb") as data_file:
        encoder.serialize_code(code_file)
        encoder.serialize_data(data_file)


def _huff_decode(
    code_output: TextIO,
    data_output: BinaryIO,
    data: str,
    info: str,
) -> None:
    decoder = time_it(HuffmanDecoder, code_output, data_output)
    if decoder.get_data() == data:
        print(f"{info}: Decoded message matches original message")
    else:
        print(f"{info}: Decoded message DOES NOT match original message")
    print()


def huffman_test(text: str, max_top_n: int) -> None:
    # words
    words_code = Path("words.json")
    words_data = Path("words.huff")
    words = list(filter(None, re.split(r"(\W+)", text)))
    time_it(_basic_huff_encode, words_code, words_data, words)
    with words_code.open("r") as c, words_data.open("rb") as d:
        _huff_decode(c, d, text, "Huffman words")

    # letters
    letters_code = Path("letters.json")
    letters_data = Path("letters.huff")
    time_it(_basic_huff_encode, letters_code, letters_data, text)
    with letters_code.open("r") as c, letters_data.open("rb") as d:
        _huff_decode(c, d, text, "Huffman letters")

    # top_n_words
    for i in range(10, max_top_n, 10):
        code = Path(f"top_{i}_words.json")
        data = Path(f"top_{i}_words.huff")
        time_it(_top_n_huff_encode, code, data, words, i)
        with code.open("r") as c, data.open("rb") as d:
            _huff_decode(c, d, text, f"Huffman top {i} words")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    args = parser.parse_args()
    input_file: Path = args.input_file
    input_text = input_file.read_text()

    arithmetic_test(input_text)
    bzip2_test(input_text, input_file)
    max_top_n = 100
    huffman_test(input_text, max_top_n)

    original_file_size = input_file.stat().st_size

    arithmetic_output_files = ["encoded_msg.ae", "decoder_helpers.ae"]
    arithmetic_size = sum(Path(x).stat().st_size for x in arithmetic_output_files)
    print("Compression Ratio for Arithmetic: ", original_file_size / arithmetic_size)

    bzip_suffixes = ["_bw_indices.pkl", "_file.bin", "_huff_dcts.pkl", "_indices.pkl", "_file_header.pkl"]
    bzip_output_files = [Path(input_file.stem + x) for x in bzip_suffixes]
    bzip_size = sum(Path(x).stat().st_size for x in bzip_output_files)
    print("Compression Ratio for Bzip2: ", original_file_size / bzip_size)

    huffman_words_size = (
        Path("words.huff").stat().st_size + Path("words.json").stat().st_size
    )
    print(
        "Compression Ratio for Huffman words: ",
        original_file_size / huffman_words_size,
    )
    huffman_letters_size = (
        Path("letters.huff").stat().st_size + Path("letters.json").stat().st_size
    )
    print(
        "Compression Ratio for Huffman letters: ",
        original_file_size / huffman_letters_size,
    )
    for i in range(10, max_top_n, 10):
        huffman_grouped_size = (
            Path(f"top_{i}_words.huff").stat().st_size
            + Path(f"top_{i}_words.json").stat().st_size
        )
        print(
            f"Compression Ratio for Huffman grouped {i}: ",
            original_file_size / huffman_grouped_size,
        )


if __name__ == "__main__":
    main()
