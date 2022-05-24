

class Transaction:
    def __init__(self, sender_wallet_id, recipient_wallet_id, amount):
        self.sender_wallet_id = sender_wallet_id
        self.recipient_wallet_id = recipient_wallet_id
        self.amount = amount

    def sign_transaction(self, transaction):
        pass

    def get_dict(self):
        return {
            "sender_wallet_id": self.sender_wallet_id,
            "recipient_wallet_id": self.recipient_wallet_id,
            "amount": self.amount
        }


