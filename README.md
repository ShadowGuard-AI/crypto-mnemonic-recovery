![Banner](banner.png)

# crypto-mnemonic-recovery

Recovers a BIP39 mnemonic phrase when some words are missing. Give the known words in order with `?` in each missing position; the tool tries every wordlist word in those positions and prints the completions whose BIP39 checksum validates.

That is the whole method: exhaustive replacement plus checksum validation. It does not do fuzzy matching, does not fix a misspelled known word, and cannot help if the position of a missing word is unknown. Each missing word multiplies the search by 2048, so one missing word is quick and three is not practical.

## Requirements

- Python 3
- The `mnemonic` package (see requirements.txt). Earlier requirements named `cryptography`, which this code does not use, and omitted the package it does use.

## Install

```bash
git clone https://github.com/ShadowGuard-AI/crypto-mnemonic-recovery.git
cd crypto-mnemonic-recovery
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py --partial_mnemonic "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ?" --num_missing 1
```

## Parameters

- `--partial_mnemonic`: The partial phrase, space separated, with `?` for each missing word. The total word count must be 12, 15, 18, 21, or 24.
- `--num_missing`: Number of missing words; must equal the number of `?` entries.
- `--language`: Mnemonic language (default: english).
- `--max_attempts`: Maximum candidates to check before stopping (default: 10000).
- `--debug`: Enable debug logging.

## License

Copyright (c) ShadowStrikeHQ
