import heapq
from collections import Counter

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoder:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def calculate_frequency(self, text):
        return Counter(text)

    def build_huffman_tree(self, frequency):
        heap = [Node(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)
        
        if len(heap) == 1:
            node = heapq.heappop(heap)
            root = Node(freq=node.freq, left=node)
            return root

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)
        return heap[0] if heap else None

    def _generate_codes_helper(self, node, current_code):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            return
        self._generate_codes_helper(node.left, current_code + '0')
        self._generate_codes_helper(node.right, current_code + '1')

    def compress(self, text):
        if not text:
            return '', {}
        self.codes = {}
        frequency = self.calculate_frequency(text)
        root = self.build_huffman_tree(frequency)
        
        if root.left is None and root.right is None: # Edge case for single character text
             self.codes[root.char] = '0'
        else:
            self._generate_codes_helper(root, '')

        return ''.join(self.codes[char] for char in text), self.codes

    def get_compression_stats(self, original_text, compressed_text):
        original_size = len(original_text) * 8
        compressed_size = len(compressed_text)
        if original_size == 0: return 0, 0, 0
        space_saved = original_size - compressed_size
        percentage_saved = (space_saved / original_size) * 100 if original_size > 0 else 0
        return 0, space_saved, percentage_saved