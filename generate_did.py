#!/usr/bin/env python3
"""
Generate an Ed25519 did:key identity locally.

Usage:
    python3 generate_did.py init   # create a new key (run once)
    python3 generate_did.py did    # print your public DID

The private key is encrypted with a passphrase and saved to identity.pem.
Nothing is sent over the network.
"""
import getpass
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

KEY_FILE = Path("identity.pem")
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(data: bytes) -> str:
    n = int.from_bytes(data, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    leading_zeros = len(data) - len(data.lstrip(b"\x00"))
    return "1" * leading_zeros + out


def did_from_private(key: Ed25519PrivateKey) -> str:
    raw_pub = key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    # multicodec prefix for ed25519-pub is 0xed 0x01, then base58btc, then "z"
    return "did:key:z" + b58encode(b"\xed\x01" + raw_pub)


def init() -> None:
    if KEY_FILE.exists():
        sys.exit("identity.pem already exists. Running init again would overwrite your key, so I stopped.")
    pw = getpass.getpass("Passphrase for the key: ")
    if len(pw) < 8:
        sys.exit("Use a passphrase with at least 8 characters.")
    if pw != getpass.getpass("Repeat passphrase: "):
        sys.exit("Passphrases don't match.")

    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(pw.encode()),
    )
    fd = os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(pem)

    print("Key created and saved to identity.pem")
    print("Your public DID:", did_from_private(key))
    print("Back up identity.pem and your passphrase now.")


def show_did() -> None:
    if not KEY_FILE.exists():
        sys.exit("Run `python3 generate_did.py init` first.")
    pw = getpass.getpass("Passphrase: ")
    key = serialization.load_pem_private_key(KEY_FILE.read_bytes(), pw.encode())
    print(did_from_private(key))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "init":
        init()
    elif cmd == "did":
        show_did()
    else:
        print(__doc__)
