import cryptography
from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.exceptions import InvalidSignature

class Signature:
    _signature: bytes

    def __init__(self, signature: bytes):
        self._signature = signature

    @staticmethod
    def Sign(data: bytes, private_key: ed448.Ed448PrivateKey) -> 'Signature':
        """
        Sign bytes using given private key.
        """
        return Signature(private_key.sign(data))

    @staticmethod
    def Deserialize(signature: str) -> 'Signature':
        """
        Deserialize a hex string to a Signature object.
        """
        return Signature(bytes.fromhex(signature))

    def Verify(self, data: bytes, public_key: ed448.Ed448PublicKey) -> bool:
        try:
            public_key.verify(data, self._signature)
            return True
        except InvalidSignature:
            return False

    def Serialize(self) -> str:
        """
        Serialize the signature to a hex string.
        """
        return self._signature.hex()

    def __str__(self):
        return self._signature.hex()
