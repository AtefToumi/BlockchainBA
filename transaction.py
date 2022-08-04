import collections

from crypto import hash, sign, verify_signature
from wallet import Wallet


class Transaction:
    def __init__(self, sender_wallet, recipient_wallet, amount):
        self.sender_wallet = sender_wallet
        self.sender_wallet_public_key = sender_wallet.public_key.exportKey().hex()
        self.recipient_wallet = recipient_wallet
        self.amount = amount

    def sign_transaction(self):
        # print(self.to_dict_sign())
        hashed_transaction = hash(self.to_dict_sign())
        # print("hashed transaction for signing : ", hashed_transaction.hexdigest())
        signature = sign(self.sender_wallet.private_key, hashed_transaction)
        setattr(self, 'signature', signature)

    def to_dict(self):
        return {
            "sender_wallet_ID": self.sender_wallet.id,
            "sender_wallet_public_key" : self.sender_wallet_public_key,
            "recipient_wallet_ID": self.recipient_wallet.id,
            "amount": self.amount,
            "signature": self.signature.hex()
        }

    def to_dict_sign(self):
        return {
            "sender_wallet_ID": self.sender_wallet.id,
            "sender_wallet_public_key": self.sender_wallet_public_key,
            "recipient_wallet_ID": self.recipient_wallet.id,
            "amount": self.amount
        }

    def to_print(self):
        return {
            "sender_wallet_ID" : self.sender_wallet.id,
            "recipient_wallet_ID": self.recipient_wallet.id,
            "amount": self.amount
        }

def verify_transaction(transaction, sender_wallet_public_key, signature ):
    hashed_transaction = hash(transaction)
    # print("hashed transaction for verifying : ", hashed_transaction.hexdigest())
    try:
        verify_signature(sender_wallet_public_key, hashed_transaction, signature)
        print("Signature is valid")
        return True
    except(ValueError, TypeError):
        print("Signature is invalid")
        return False

# w1 = Wallet(1)
# w2 = Wallet(2)
# t = Transaction(w1, w2, 20)
# t.sign_transaction()
# t.verify_transaction()
# print(t.to_dict())
