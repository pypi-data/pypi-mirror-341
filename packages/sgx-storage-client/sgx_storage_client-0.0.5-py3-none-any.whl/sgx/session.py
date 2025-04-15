import base64
import secrets
import socket
import json
from typing import Optional

from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from sgx.attestaion import SGXAttestationVerifier
from sgx.ecdh_provider import ECDHProvider

KDF_ID = b"\x01\x00"
CURVE = ec.SECP256R1()
MSG_TERMINATOR = b'}'


class SecureMessageHandler:

    def receive_msg(self, sock: socket.socket) -> dict:
        """
        Receives complete JSON messages using SGX-specific message framing

        Cryptographic Role:
            - Message boundary detection using '}' terminator
            - Prevents partial message processing attacks

        Process:
            1. Accumulates network data until terminator byte is found
            2. Validates non-empty message
            3. Decodes UTF-8 JSON payload

        Returns:
            dict: Parsed JSON message

        Raises:
            ConnectionError: On empty message or premature connection closure
        """
        json_bytes = bytearray()
        while True:
            data = sock.recv(4096).strip()
            if not data:
                break
            json_bytes.extend(data)
            if data.endswith(MSG_TERMINATOR):
                break

        if not json_bytes:
            raise ConnectionError("Empty response")

        return json.loads(json_bytes.decode('utf-8'))

    def send_msg(self, sock: socket.socket, msg: dict) -> None:
        """
        Sends JSON messages with SGX-protocol framing

        Cryptographic Role:
            - Ensures message atomicity
            - Maintains protocol synchronization

        Process:
            1. Serializes dict to JSON
            2. Appends MSG_TERMINATOR (b'})
            3. Uses atomic sendall() for transmission
        """
        json_str = json.dumps(msg)
        sock.sendall(json_str.encode() + MSG_TERMINATOR)

    def create_signature(self, challenger_pub: bytes, enclave_pub: bytes, private_value: int) -> bytes:
        """
        Generates ECDSA signature for enclave authentication

        Cryptographic Method:
            - ECDSA with SHA-256 over SECP256R1
            - SGX-specific byte reversal of public key components

        Process:
            1. Reverses byte order of both public keys (32-byte chunks)
            2. Signs concatenated reversed public keys
            3. Converts DER signature to raw 64-byte format (R||S)

        Args:
            challenger_pub: 64-byte client public key
            enclave_pub: 64-byte enclave public key

        Returns:
            64-byte raw signature (32-byte R || 32-byte S)
        """
        g_b = challenger_pub[:32][::-1] + challenger_pub[32:][::-1]
        g_a = enclave_pub[:32][::-1] + enclave_pub[32:][::-1]

        ec_priv = ec.derive_private_key(private_value, CURVE, default_backend())
        der_sig = ec_priv.sign(g_b + g_a, ec.ECDSA(hashes.SHA256()))
        r, s = utils.decode_dss_signature(der_sig)
        return r.to_bytes(32, 'big') + s.to_bytes(32, 'big')

    def derive_key(self, shared_secret: bytes, label: bytes) -> bytes:
        """"
        Derives session keys using SGX-specific CMAC-KDF

        Cryptographic Method:
            - CMAC-based Key Derivation Function (KDF)
            - SP 800-108 compliant with SGX-specific modifications

        Process:
            1. Reverses shared secret bytes (SGX endianness requirement)
            2. Two-step CMAC process:
               - First CMAC with empty key creates intermediate key
               - Second CMAC with derivation string

        Args:
            label: Key purpose label (b'SMK' for MAC, b'SK' for encryption)

        Returns:
            16-byte derived key for specified purpose
        """
        reversed_key = shared_secret[::-1]
        empty_key = b'\x00' * 16

        # First CMAC
        cobj = CMAC.new(empty_key, ciphermod=AES)
        cobj.update(reversed_key)
        tmp_key = cobj.digest()

        # Derivation string
        derivation = b'\x01' + label + b'\x00' + b'\x80\x00'

        # Second CMAC
        cobj = CMAC.new(tmp_key, ciphermod=AES)
        cobj.update(derivation)
        return cobj.digest()

    def generate_mac(
            self, mac_key: bytes, pub_key: bytes, spid: bytes, quote_type: bytes, kdf_id: bytes, signature: bytes
    ) -> bytes:
        """
        Generates CMAC for MSG2 authentication

        Cryptographic Method:
            - AES-CMAC (RFC 4493)
            - SGX-specific byte reversal of public key and signature

        Process:
            1. Reverses 32-byte chunks of public key and signature
            2. Constructs authentication blob:
               reversed_pub || spid || quote_type || kdf_id || reversed_sig
            3. Computes CMAC over concatenated data

        Returns:
            16-byte authentication tag
        """
        reversed_pub = pub_key[:32][::-1] + pub_key[32:][::-1]
        reversed_sig = signature[:32][::-1] + signature[32:][::-1]
        auth_data = reversed_pub + spid + quote_type + kdf_id + reversed_sig

        cobj = CMAC.new(mac_key, ciphermod=AES)
        cobj.update(auth_data)
        return cobj.digest()

    def encrypt_payload(self, payload: dict, shared_key: bytes) -> tuple[bytes, bytes]:
        """
        Encrypts payload using AES-GCM authenticated encryption

        Cryptographic Method:
            - AES-128-GCM (NIST SP 800-38D)
            - Provides confidentiality and integrity

        Process:
            1. Derives encryption key from shared secret
            2. Generates random 12-byte nonce
            3. Encrypts JSON payload with associated data

        Returns:
            tuple: (ciphertext_with_tag, nonce)
        """
        key = self.derive_key(shared_key, b'SK')
        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = json.dumps(payload).encode()
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext + tag, nonce

    def decrypt_payload(self, nonce: bytes, ciphertext: bytes, shared_key: bytes) -> bytes:
        """
        Decrypts and verifies AES-GCM payload

        Cryptographic Method:
            - AES-128-GCM with 128-bit authentication tag
            - Validates ciphertext integrity

        Returns:
            Decrypted plaintext payload

        Raises:
            CryptoError: On authentication failure
        """
        key = self.derive_key(shared_key, b'SK')
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        tag = ciphertext[-16:]
        data = ciphertext[:-16]
        return cipher.decrypt_and_verify(data, tag)


class SgxSession:
    def __init__(
            self,
            method: str,
            params: dict,
            host: str,
            port: int,
            spid: str,
            key_provider: ECDHProvider,
            attestation_verifier: Optional[SGXAttestationVerifier] = None
    ):
        """
        Initializes SGX DCAP attestation client

        Args:
            method: RPC method to execute after attestation
            params: Method parameters for encrypted request
            host: Enclave host address
            port: Enclave port
            spid: Service Provider ID (16-byte hex string)
            key_provider: Private key provider for enclave authentication
            attestation_verifier: Optional attestation verifier
        """
        self.utils = SecureMessageHandler()
        self.method = method
        self.params = params
        self.host = host
        self.port = port
        self.key_provider = key_provider
        self.spid = bytes.fromhex(spid)
        self.attestation_verifier = attestation_verifier
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)

    def __enter__(self):
        """Context manager for socket connection handling"""
        self.socket.connect((self.host, self.port))
        return self

    def __exit__(self, *exc):
        """Ensures proper socket cleanup"""
        self.socket.close()

    def execute(self) -> str:
        """
        Executes full SGX DCAP attestation protocol flow

        Protocol Steps:
            1. MSG0: Initiate attestation request
            2. MSG1: Receive enclave public key and verify enclave via quote data
            3. MSG2: Perform ECDH key exchange + send signature
            4. MSG3: Receive attestation evidence (quote)
            5. MSG4: Send encrypted RPC request
            6. Receive and decrypt final response

        Cryptographic Sequence:
            - Ephemeral ECDH key exchange
            - ECDSA enclave authentication
            - CMAC-based session key derivation
            - AES-GCM encrypted payloads

        Returns:
            Decrypted response from enclave service

        Raises:
            AttestationError: For protocol violations or verification failures
        """
        try:
            # MSG0: Attestation request
            self.socket.sendall(b'{"jsonrpc":"2.0","id":0,"method":"attest_DCAP"}')

            # MSG1: Receive enclave public key and verify enclave
            msg0 = self.utils.receive_msg(self.socket)
            enclave_pub = bytes(msg0['result']['public_key'])
            if self.attestation_verifier is not None:
                self.attestation_verifier.verify(
                    msg0['result']['quote'],
                    nonce=base64.b64encode(secrets.token_bytes(16)).decode('utf-8')
                )

            client_pub = self.key_provider.get_ephemeral_public_key()
            shared_key = self.key_provider.derive_shared_secret(enclave_pub)
            signature = self.key_provider.sign_challenge(client_pub, enclave_pub)

            mac_key = self.utils.derive_key(shared_key, b'SMK')
            mac = self.utils.generate_mac(mac_key, client_pub, self.spid, b"\x01\x00", KDF_ID, signature)

            # Send MSG2
            msg2 = {
                "id": 2,
                "method": "msg2",
                "params": {
                    "public_key": client_pub.hex(),
                    "spid": self.spid.hex(),
                    "quote_type": "0100",
                    "kdf_id": KDF_ID.hex(),
                    "key_signature": signature.hex(),
                    "mac": mac.hex(),
                    "revocation_list": ""
                }
            }
            self.utils.send_msg(self.socket, msg2)

            # MSG3: Receive attestation evidence
            msg3 = self.utils.receive_msg(self.socket)
            if 'error' in msg3:
                raise RuntimeError(f"Attestation failed: {msg3['error']}")

            # MSG4: Send encrypted request
            payload = {"id": 4, "method": self.method, "params": self.params}
            ciphertext, nonce = self.utils.encrypt_payload(payload, shared_key)

            msg4 = {
                "id": 4,
                "method": "msg4",
                "params": {
                    "nonce": nonce.hex(),
                    "ct": ciphertext.hex()
                }
            }
            self.utils.send_msg(self.socket, msg4)

            # Get final response
            response = self.utils.receive_msg(self.socket)
            if 'error' in response:
                raise RuntimeError(f"Request failed: {response['error']}")

            # Decrypt response
            ciphertext = bytes.fromhex(response['result']['ct'])
            nonce = bytes.fromhex(response['result']['nonce'])
            decrypted = self.utils.decrypt_payload(nonce, ciphertext, shared_key)

            return decrypted.decode()

        except KeyError as e:
            raise RuntimeError("Missing expected field in response") from e
