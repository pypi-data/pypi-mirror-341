from typing import Protocol

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils

KDF_ID = b"\x01\x00"
CURVE = ec.SECP256R1()
MSG_TERMINATOR = b'}'


class ECDHProvider(Protocol):
    def get_ephemeral_public_key(self) -> bytes: ...
    def derive_shared_secret(self, peer_public: bytes) -> bytes: ...
    def sign_challenge(self, challenger_pub: bytes, enclave_pub: bytes) -> bytes: ...


class RawPrivateKeyProvider:
    def __init__(self, private_value: int):
        self.private_value = private_value
        self.curve = ec.SECP256R1()
        self._ephemeral_key = ec.generate_private_key(self.curve, default_backend())

    def get_ephemeral_public_key(self) -> bytes:
        pub_nums = self._ephemeral_key.public_key().public_numbers()
        return pub_nums.x.to_bytes(32, 'big') + pub_nums.y.to_bytes(32, 'big')

    def derive_shared_secret(self, peer_public: bytes) -> bytes:
        """
        Computes ECDH shared secret for session key derivation

        Cryptographic Method:
            - Elliptic Curve Diffie-Hellman key exchange
            - NIST SP 800-56A compliant implementation

        Process:
            1. Reconstructs peer's public key from X/Y coordinates
            2. Performs ECDH computation using local private key

        Returns:
            32-byte shared secret for key derivation
        """
        x = int.from_bytes(peer_public[:32], 'big')
        y = int.from_bytes(peer_public[32:], 'big')
        peer_pub = ec.EllipticCurvePublicNumbers(x, y, self.curve).public_key(default_backend())
        return self._ephemeral_key.exchange(ec.ECDH(), peer_pub)

    def sign_challenge(self, challenger_pub: bytes, enclave_pub: bytes) -> bytes:
        g_b = challenger_pub[:32][::-1] + challenger_pub[32:][::-1]
        g_a = enclave_pub[:32][::-1] + enclave_pub[32:][::-1]
        ec_priv = ec.derive_private_key(self.private_value, self.curve, default_backend())
        der_sig = ec_priv.sign(g_b + g_a, ec.ECDSA(hashes.SHA256()))
        r, s = utils.decode_dss_signature(der_sig)
        return r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
