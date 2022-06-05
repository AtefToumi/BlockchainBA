import collections

from crypto import hash, sign


class Transaction:
    def __init__(self, sender_wallet_id, recipient_wallet_id, amount):
        self.sender_wallet_id = sender_wallet_id
        self.recipient_wallet_id = recipient_wallet_id
        self.amount = amount

    def sign_transaction(self, sender_public_key):
        hashed_transaction = hash(self.to_dict_sign())
        signature = sign(sender_public_key, hashed_transaction)
        setattr(self, 'signature', signature)

    def to_dict(self):
        return collections.OrderedDict({
            "sender_wallet_id": self.sender_wallet_id,
            "recipient_wallet_id": self.recipient_wallet_id,
            "amount": self.amount,
            "signature": self.signature.hex()
        })
    def to_dict_sign(self):
        return collections.OrderedDict({
            "sender_wallet_id": self.sender_wallet_id,
            "recipient_wallet_id": self.recipient_wallet_id,
            "amount": self.amount
        })
