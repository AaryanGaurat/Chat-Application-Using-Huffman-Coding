from huffman_coding import HuffmanCoder
from chat_message import CompressedChatMessage

class HuffmanChatSystem:
    def __init__(self):
        self.huffman_coder = HuffmanCoder()
        self.message_history = []

    def create_message(self, sender, text):
        compressed_text, codes = self.huffman_coder.compress(text)
        return CompressedChatMessage(sender, text, compressed_text, codes)

    def decompress_message(self, compressed_msg):
        reverse_codes = {v: k for k, v in compressed_msg.codes.items()}
        current_code = ""
        decoded_text = ""
        for bit in compressed_msg.compressed_data:
            current_code += bit
            if current_code in reverse_codes:
                decoded_text += reverse_codes[current_code]
                current_code = ""
        compressed_msg.original_text = decoded_text
        return compressed_msg
        
    def add_to_history(self, message):
        self.message_history.append(message)