import hashlib
import json

class Transaction:
    amount: int
    fees: int
    recipient: str
    sender: str

    def __init__(self, amount: int, fees: int, recipient: str, sender: str):
        self.amount = amount
        self.fees = fees
        self.recipient = recipient
        self.sender = sender

    @staticmethod
    def FromDict(data: dict) -> "Transaction":
        """
        Create a Transaction object from a dictionary.
        """
        return Transaction(
            amount=data["amount"],
            fees=data["fees"],
            recipient=data["recipient"],
            sender=data["sender"],
        )

    @staticmethod
    def Deserialize(json_str: str) -> "Transaction":
        """
        Create a Transaction object from a JSON string.
        """
        data = json.loads(json_str)
        return Transaction.FromDict(data)

    def ToDict(self) -> dict:
        """
        Serialize the transaction to a dict.
        """
        return {
            "amount": self.amount,
            "fees": self.fees,
            "recipient": self.recipient,
            "sender": self.sender,
        }

    def Serialize(self) -> str:
        """
        Serialize the transaction to a JSON string.
        """
        return json.dumps(Transaction.ToDict(self), indent=None, separators=(',', ':'))

    def __str__(self) -> str:
        """
        String representation of the transaction.
        """
        return self.Serialize()

    def GetHash(self) -> str:
        """
        Get the hash of the transaction.
        """
        return hashlib.sha3_256(Transaction.Serialize(self).encode()).hexdigest()