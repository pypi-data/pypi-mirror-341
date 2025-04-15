import os
import secrets
from typing import Tuple, Sequence

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import hmac
import hashlib


SEED_ITERATIONS = 2048
CURVE = ec.SECP256R1()
SEED = b"Bitcoin seed"
SALT = b"mnemonic"


def pbkdf2_seed(passphrase: str, salt: bytes = SALT, iterations: int = SEED_ITERATIONS) -> bytes:
    """
    Derives a cryptographic seed from a passphrase using PBKDF2-HMAC-SHA512.

    Args:
        passphrase (str): The passphrase to derive the seed from.
        salt (bytes): The salt to use in the key derivation function.
        iterations (int): The number of iterations for PBKDF2.

    Returns:
        bytes: A 64-byte derived seed.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=64,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(passphrase.encode())


def create_scalar(key: bytes, seed: bytes) -> int:
    """
    Derives a scalar integer from a seed using HMAC-SHA512.

    Args:
        key (bytes): The HMAC key, typically a constant.
        seed (bytes): The input seed from which the scalar is derived.

    Returns:
        int: The resulting scalar as a big-endian integer.
    """
    digest = hmac.new(key, seed, hashlib.sha512).digest()
    return int.from_bytes(digest[:32], byteorder='big')


def get_private_key_from_scalar(scalar: int) -> ec.EllipticCurvePrivateKey:
    """
    Constructs an EC private key object from a scalar integer.

    Args:
        scalar (int): The private scalar value.

    Returns:
        ec.EllipticCurvePrivateKey: The corresponding private key.
    """
    return ec.derive_private_key(scalar, CURVE, default_backend())


def get_public_key_bytes_from_scalar(scalar: int) -> bytes:
    """
    Derives the public key bytes from a private scalar.

    Args:
        scalar (int): The private scalar value.

    Returns:
        bytes: The concatenated X and Y coordinates of the public key (64 bytes).
    """
    private_key = get_private_key_from_scalar(scalar)
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()
    x = numbers.x.to_bytes(32, 'big')
    y = numbers.y.to_bytes(32, 'big')
    return x + y


def generate_key_pair_from_passphrase(passphrase: str) -> tuple[bytes, int]:
    """
    Generates an EC key pair deterministically from a passphrase.

    Args:
        passphrase (str): The passphrase to generate the key pair from.
        validate (bool): Use passphrase value validation or not.

    Returns:
        tuple[bytes, int]: A tuple containing the public key bytes (X||Y) and the private scalar.
    """
    seed = pbkdf2_seed(passphrase)
    scalar = create_scalar(SEED, seed)
    public_key_bytes = get_public_key_bytes_from_scalar(scalar)
    return public_key_bytes, scalar


def load_wordlist() -> list[str]:
    """Load wordlist.txt and return list of words."""
    base_path = os.path.dirname(__file__)
    wordlist_path = os.path.join(base_path, "wordlist.txt")
    words = []
    with open(wordlist_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                words.append(parts[1])
    return words


def generate_passphrase(
    *,
    num_words: int = 6,
    wordlist: Sequence[str] | None = None,
    delimiter: str = " ",
    capitalize: bool = False,
    add_number: bool = False,
    rng: secrets.SystemRandom | None = None,
) -> str:
    """
    Return (passphrase, estimated_entropy_bits).

    • num_words   – 5–7 is typical; ↑ words = ↑ entropy
    • wordlist    – sequence of candidate words (default: Diceware list)
    • delimiter   – "-" / " " / "" etc.
    • capitalize  – Title‑case each word (tiny security gain, big readability gain)
    • add_number  – append one random digit (≈ 3.3 bits)
    """

    if rng is None:
        rng = secrets.SystemRandom()          # uses /dev/urandom or CryptGenRandom

    if wordlist is None:
        wordlist = load_wordlist()            # ~7 776 words by default

    if num_words < 1:
        raise ValueError("num_words must be ≥ 1")

    words = [rng.choice(wordlist) for _ in range(num_words)]
    if capitalize:
        words = [w.capitalize() for w in words]

    passphrase = delimiter.join(words)

    if add_number:
        passphrase += str(rng.randrange(10))

    return passphrase
