from crypto import create_key, import_public_key
from uuid import uuid4
import collections

class Node:
    def __init__(self):
        # Generate a globally unique address for this node
        self.node_identifier = str(uuid4()).replace('-', '')
        self.private_key = create_key()
        self.public_key = import_public_key(self.private_key)
        
    def to_dict(self):
        return collections.OrderedDict({
            "node_identifier": self.node_identifier,
            "public_key": self.public_key.exportKey().hex(),
        })

    
