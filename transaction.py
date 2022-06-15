import collections

from crypto import hash, sign,verify_signature


class Transaction:
    def __init__(self, sender_wallet, recipient_wallet, amount):
        self.sender_wallet = sender_wallet
        self.recipient_wallet = recipient_wallet
        self.amount = amount

    def sign_transaction(self):
        hashed_transaction = hash(self.to_dict_sign())
        signature = sign(self.sender_wallet.private_key, hashed_transaction)
        setattr(self, 'signature', signature)

    def verify_transaction(self):
        hashed_transaction = hash(self.to_dict_sign())
        try:
            verify_signature(self.sender_wallet.public_key, hashed_transaction, self.signature)
            return True
        except(ValueError, TypeError):
            return False


    def to_dict(self):
        return collections.OrderedDict({
            "sender_wallet_ID": self.sender_wallet.id,
            "recipient_wallet_ID": self.recipient_wallet.id,
            "amount": self.amount,
            "signature": self.signature.hex()
        })
    def to_dict_sign(self):
        return collections.OrderedDict({
            "sender_wallet_ID": self.sender_wallet.id,
            "recipient_wallet_ID": self.recipient_wallet.id,
            "amount": self.amount
        })
