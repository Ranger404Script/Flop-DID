# Creating a Technocore DID (did:key)

A quick guide to generating an Ed25519 `did:key` identity on your own machine, so you're ready for the FLOP testnet.

This is an unofficial guide and I'm not affiliated with Flop Labs. Making a DID doesn't guarantee an airdrop. From what's been said publicly, rewards depend on testnet activity, so keep an eye on the official @flop_labs and @CryptoHayes accounts for the real rules.

## What a DID is here

It's just an Ed25519 keypair. Your public key gets wrapped into an identifier that looks like this:

```
did:key:z6Mk...
```

You keep the private key and use it to sign messages. The DID is public, and anyone can use it to check that a signature came from you.

Under the hood, the DID is the raw 32-byte public key with a multicodec prefix (`0xed01`), encoded in base58btc, with a `z` in front. That's why every Ed25519 DID starts with `z6Mk`.

## What you need

- Python 3.8 or newer
- The `cryptography` package

```bash
pip install cryptography
```

## Step 1: Generate your key

```bash
python3 generate_did.py init
```

It asks for a passphrase, encrypts your private key, saves it to `identity.pem`, and prints your DID.

Only run this once. If `identity.pem` already exists the script refuses to continue, so you can't wipe your key by accident.

To see your DID again later:

```bash
python3 generate_did.py did
```

## Step 2: Back it up

Do this right away. If you lose `identity.pem` or the passphrase, you lose control of the identity, and probably the airdrop that goes with it.

- Copy `identity.pem` to a couple of different places (USB drive, external disk, password manager)
- Store the passphrase somewhere separate from the file
- Don't leave the only copy on your phone or a single laptop

## Step 3: Register and check in

This part happens on Technocore (technocore.chat):

1. Publish your public DID to the Technocore registry
2. Sign a check-in message with your private key and send it

The exact API and signing format can change, so follow the official Flop Labs instructions and their signer tool for this step instead of copying random scripts. If any tool asks for your private key, read its source code first.

## Security rules

- Never upload `identity.pem` to GitHub. The `.gitignore` in this repo blocks it, but double-check before every commit.
- Never send your key or passphrase to anyone, including people claiming to be support or team members. The real team doesn't need your private key.
- Never paste your key into a website you don't fully trust.
- Only share the public DID.
- If a key ever leaks, stop using it and generate a new one.

## What comes next

Based on public info so far:

- Airdrop allocation is tied to testnet activity: claim test tokens from the faucet, then actually spend them on inference
- Miner, validator and KOL roles are applied for through the official site
- Reported timeline is a testnet in Q4 2026 and mainnet in Q1 2027, but dates may shift

## Files

```
generate_did.py   # creates and shows your DID
.gitignore        # keeps the private key out of git
README.md         # this guide
```

## License

Use at your own risk. Not financial advice


 ## About me

- DID:z6MksnizCG1qBxYyRyChKbgkkyGY1DTTZC3U7pn21PSQUWDF
- X: https://x.com/_hadiew

 
