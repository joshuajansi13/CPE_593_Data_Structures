# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)


def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d


# Test Huffman encoding
input_str = input("Please input your string: ")

# Calculating frequency
freq = {}
for c in input_str:
    if c in freq:
        freq[c] += 1
    else:
        freq[c] = 1

freq_list = list(freq.items())
freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

huffmanCode = huffman_code_tree(nodes[0][0])

print(' Char | Huffman code ')
print('----------------------')
huffmanCodeFreq = []
for (char, frequency) in freq_list:
    huffmanCodeChar = huffmanCode[char]
    huffmanCodeFreq.append((huffmanCodeChar, frequency))
    print(' %-4r |%12s' % (char, huffmanCodeChar))

encondingStr = ""
for (char, frequency) in huffmanCodeFreq:
    encondingStr += char*frequency

print(f"The encoding string of the original input: {encondingStr}")