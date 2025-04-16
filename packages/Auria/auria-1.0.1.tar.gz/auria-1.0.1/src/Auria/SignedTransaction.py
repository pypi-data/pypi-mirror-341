import json
from cryptography.hazmat.primitives.asymmetric import ed448
from typing_extensions import override

from .Wallet import Wallet
from .Transaction import Transaction
from .Signature import Signature


class SignedTransaction(Transaction):
    _signature: Signature
    _public_key: ed448.Ed448PublicKey

    def __init__(self, transaction: Transaction, wallet: Wallet):
        super().__init__(transaction.amount, transaction.fees, transaction.recipient, transaction.sender)
        self._signature = Signature.Sign(transaction.GetHash().encode(), wallet.GetPrivateKey())
        self._public_key = wallet.GetPublicKey()

    @override
    def ToDict(self) -> dict:
        return {
            "transaction": super().ToDict(),
            "hash": self.GetHash(),
            "pubkey": f"{self._public_key.public_bytes_raw().hex()}",
            "signature": self._signature.Serialize(),
        }

    @override
    def Serialize(self) -> str:
        """
        Serialize the signed transaction to a JSON string.
        """
        # return json.dumps(self.ToDict(), indent=None, separators=(',', ':'))  # currently not necessary
        return json.dumps(self.ToDict())