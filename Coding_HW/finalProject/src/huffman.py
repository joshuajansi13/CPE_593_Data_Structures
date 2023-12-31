import heapq
import json
import pickle
from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Iterable
from itertools import chain
from typing import BinaryIO, Self, TextIO

from bitarray import bitarray


class _HuffmanNode:
    count: int
    data: str
    left: Self | None
    right: Self | None

    def __init__(
        self: Self,
        count: int,
        data: str,
        left: Self | None = None,
        right: Self | None = None,
    ) -> None:
        self.count = count
        self.data = data
        self.left = left
        self.right = right

    def __lt__(self: Self, other: Self) -> bool:
        return self.count < other.count


class _HuffmanEncoder(ABC):
    @abstractmethod
    def code(self: Self) -> dict[str, bitarray]:
        pass

    @abstractmethod
    def source(self: Self) -> Iterable[str]:
        pass

    def serialize_data(self: Self, output: BinaryIO) -> None:
        bits = bitarray()
        bits.encode(self.code(), self.source())
        pickle.dump(bits, output)

    def serialize_code(self: Self, output: TextIO) -> None:
        n = {k: v.to01() for k, v in self.code().items()}
        json.dump(n, output)


class BasicHuffmanEncoder(_HuffmanEncoder):
    _source: list[str]
    _code: dict[str, bitarray]

    def __init__(self: Self, source: Iterable[str]) -> None:
        self._source = list(source)
        self._code = {}
        root = self._build_tree()
        self._build_code(root, "")

    def _build_tree(self: Self) -> _HuffmanNode:
        frequencies = Counter(self._source)
        priority_queue: list[_HuffmanNode] = []
        for data, count in frequencies.items():
            heapq.heappush(priority_queue, _HuffmanNode(count, data))

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            node = _HuffmanNode(left.count + right.count, "", left, right)
            heapq.heappush(priority_queue, node)

        return priority_queue[0]

    def _build_code(self: Self, node: _HuffmanNode, arr: str) -> None:
        if node.data:
            self._code[node.data] = bitarray(arr)
            return
        if node.left is not None and node.right is not None:
            self._build_code(node.left, arr + "0")
            self._build_code(node.right, arr + "1")

    def code(self: Self) -> dict[str, bitarray]:
        return self._code

    def source(self: Self) -> Iterable[str]:
        return self._source


class HybridHuffmanEncoder(_HuffmanEncoder):
    _source_words: list[str]
    _code: dict[str, bitarray]

    def __init__(self: Self, words: list[str], num_most_common: int = 10) -> None:
        self._source_words = words
        self._code = {}
        root = self._build_tree(num_most_common)
        self._build_code(root, "")

    def _build_tree(self: Self, num_most_common: int) -> _HuffmanNode:
        word_frequencies = Counter(word for word in self._source_words if len(word) > 1)
        most_common_words = word_frequencies.most_common(num_most_common)
        chars = list(chain(*self._source_words))
        char_frequencies = Counter(chars)

        priority_queue: list[_HuffmanNode] = []
        for data, count in most_common_words:
            heapq.heappush(priority_queue, _HuffmanNode(count, data))
        for data, count in char_frequencies.items():
            heapq.heappush(priority_queue, _HuffmanNode(count, data))

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            node = _HuffmanNode(left.count + right.count, "", left, right)
            heapq.heappush(priority_queue, node)

        return priority_queue[0]

    def _build_code(self: Self, node: _HuffmanNode, arr: str) -> None:
        if node.data:
            self._code[node.data] = bitarray(arr)
            return
        if node.left is not None and node.right is not None:
            self._build_code(node.left, arr + "0")
            self._build_code(node.right, arr + "1")

    def code(self: Self) -> dict[str, bitarray]:
        return self._code

    def source(self: Self) -> Iterable[str]:
        return self._source_words

    def serialize_data(self: Self, output: BinaryIO) -> None:
        bits = bitarray()
        for word in self._source_words:
            if word in self._code:
                bits.extend(self._code[word])
            else:
                for char in word:
                    bits.extend(self._code[char])
        pickle.dump(bits, output)


class HuffmanDecoder:
    _code: dict[str, bitarray]
    _data: str

    def __init__(self: Self, code_file: TextIO, data_file: BinaryIO) -> None:
        self._code = {k: bitarray(v) for k, v in json.load(code_file).items()}
        data = pickle.load(data_file)
        data = data.decode(self._code)
        self._data = "".join(data)

    def get_data(self: Self) -> str:
        return self._data
