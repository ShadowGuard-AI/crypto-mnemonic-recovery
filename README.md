![Introduction banner: the themed scene before any name is spoken](intro-banner.png)

# crypto-mnemonic-recovery

Title block: the name above is the first entry in a night watch log, set in BioRhyme Expanded in eye gold on an owl brown plate, with an hour note at its left margin, a ruled line beneath, and a small pellet drawn once beside the first heading and nowhere else.

![Logo](logo.png)

![Wordmark banner](banner.png)

![Animated scene](scene.svg)

![Major separator](sep-heavy.svg)


# crypto-mnemonic-recovery

Recovers a BIP39 mnemonic phrase when some words are missing. Give the known words in order with `?` in each missing position; the tool tries every wordlist word in those positions and prints the completions whose BIP39 checksum validates.

That is the whole method: exhaustive replacement plus checksum validation. It does not do fuzzy matching, does not fix a misspelled known word, and cannot help if the position of a missing word is unknown. Each missing word multiplies the search by 2048, so one missing word is quick and three is not practical.

![Major separator](sep-heavy.svg)

## Requirements

- Python 3
- The `mnemonic` package (see requirements.txt). Earlier requirements named `cryptography`, which this code does not use, and omitted the package it does use.

![Minor separator](sep-light.svg)

## Install

```bash
git clone https://github.com/ShadowGuard-AI/crypto-mnemonic-recovery.git
cd crypto-mnemonic-recovery
pip install -r requirements.txt
```


> Watch note, entered at the hour: the declared missing count must equal the number of question mark places actually present, and a disagreement ends the run at exit 1.

![Minor separator](sep-light.svg)

## Usage

The live README usage block stands at this place in the original file. Under the secrets rule that governs this repository it is described here, not reproduced: the block runs python3 main.py with the partial phrase control set to a partial phrase of eleven known entries in order and one question mark in the final place, and the missing count control set to 1. No entry from any phrase appears in this document or on the site.


> Watch note, entered at the hour: under the default ceiling of 10000, a search with two missing places is interrupted long before its field of a little over four million candidates is exhausted.

![Minor separator](sep-light.svg)

## Parameters

- `--partial_mnemonic`: The partial phrase, space separated, with `?` for each missing word. The total word count must be 12, 15, 18, 21, or 24.
- `--num_missing`: Number of missing words; must equal the number of `?` entries.
- `--language`: Mnemonic language (default: english).
- `--max_attempts`: Maximum candidates to check before stopping (default: 10000).
- `--debug`: Enable debug logging.


> Watch note, entered at the hour: an empty result after such an interruption records only that no valid completion appeared among the candidates actually checked, not that none exists in the unsearched remainder.

![Minor separator](sep-light.svg)

## Verified run note

`--help` was verified live in this wave. A full recovery run is blocked here because the `mnemonic` package is not installed, and installs are forbidden in this wave; no recovery result is claimed.


> Watch note, entered at the hour: anything this tool prints on a successful run is material that restores access, and it is to be guarded as such.

![Minor separator](sep-light.svg)

## License

Licensed under the terms in LICENSE.

![Major separator](sep-heavy.svg)

## Watch notes, gathered at the close

The buttons of this re-skin read Begin the Search and Read the Watch Rules. Its controls are headed Candidates to Be Examined Before Stopping and Wordlist Language. Its result headings read Completions That Validate, No Completion Among Those Examined, and Search Stopped at the Ceiling. One further fact is entered once more: the repository LICENSE file carries the MIT License, its holder line giving a pen name together with a single initial for the remaining name.
