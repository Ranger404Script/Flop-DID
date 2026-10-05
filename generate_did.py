#!/usr/bin/env python3
"""
generate_did.py - ساخت هویت did:key (Ed25519) به‌صورت لوکال

دستورها:
    python3 generate_did.py init   # ساخت کلید جدید (فقط یک بار)
    python3 generate_did.py did    # نمایش DID عمومی

کلید خصوصی با رمز عبور رمزنگاری می‌شود و در identity.pem ذخیره می‌شود.
هیچ داده‌ای به اینترنت ارسال نمی‌شود.
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
    # multicodec ed25519-pub = 0xed 0x01  ->  base58btc  ->  پیشوند z
    return "did:key:z" + b58encode(b"\xed\x01" + raw_pub)


def init() -> None:
    if KEY_FILE.exists():
        sys.exit("identity.pem از قبل وجود دارد. دوباره init نزن، کلید قبلی از بین می‌رود.")
    pw = getpass.getpass("رمز عبور برای رمزنگاری کلید: ")
    if len(pw) < 8:
        sys.exit("رمز عبور حداقل ۸ کاراکتر باشد.")
    if pw != getpass.getpass("تکرار رمز عبور: "):
        sys.exit("رمزها یکسان نیستند.")

    key = Ed25519PrivateKey.generate()
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.BestAvailableEncryption(pw.encode()),
    )
    fd = os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(pem)

    print("کلید ساخته شد و در identity.pem ذخیره شد.")
    print("DID عمومی تو:", did_from_private(key))
    print("از identity.pem و رمز عبورش همین حالا چند نسخه‌ی پشتیبان بگیر.")


def show_did() -> None:
    if not KEY_FILE.exists():
        sys.exit("اول python3 generate_did.py init را اجرا کن.")
    pw = getpass.getpass("رمز عبور: ")
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
