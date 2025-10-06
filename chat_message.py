import json
from datetime import datetime

class CompressedChatMessage:
    def __init__(self, sender, original_text, compressed_data, codes, timestamp=None):
        self.sender = sender
        self.original_text = original_text
        self.compressed_data = compressed_data
        self.codes = codes
        self.timestamp = timestamp or datetime.now().strftime("%H:%M:%S")

    def to_dict(self):
        return {
            'sender': self.sender,
            'compressed_data': self.compressed_data,
            'codes': self.codes,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sender=data['sender'],
            original_text='',
            compressed_data=data['compressed_data'],
            codes=data['codes'],
            timestamp=data['timestamp']
        )