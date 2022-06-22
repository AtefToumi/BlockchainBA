import collections

from crypto import hash, sign,verify_signature
from wallet import Wallet


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
            print("Signature is valid")
            return True
        except(ValueError, TypeError):
            print("Signature is invalid")
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




# w1 = Wallet(1)
# w2 = Wallet(2)
# t = Transaction(w1, w2, 20)
# t.sign_transaction()
# t.verify_transaction()
# print(t.to_dict())