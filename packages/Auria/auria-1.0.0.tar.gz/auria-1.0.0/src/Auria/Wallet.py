import hashlib

from cryptography.hazmat.primitives.asymmetric import ed448
from cryptography.hazmat.primitives import serialization
import requests
import json
import base64


class Wallet:
    private_key: ed448.Ed448PrivateKey

    def __init__(self, private_key: ed448.Ed448PrivateKey):
        self.private_key = private_key

    @staticmethod
    def Generate():
        """
        Generate a new ED448 private key.
        """
        return Wallet(ed448.Ed448PrivateKey.generate())

    def GetPrivateKey(self) -> ed448.Ed448PrivateKey:
        """
        Get the private key.
        """
        return self.private_key

    def GetPublicKey(self) -> ed448.Ed448PublicKey:
        """
        Get the public key from the private key.
        """
        return self.private_key.public_key()

