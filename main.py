import argparse
import logging
import sys
from typing import Iterator, List


def _load_mnemonic_class():
    # Imported lazily, not at module top: a top level import used to make
    # even --help exit 1 on a machine without the package, so there was no
    # way to read the usage text that explains the dependency. A real run
    # still fails with the same clear message and exit 1.
    try:
        from mnemonic import Mnemonic
    except ImportError:
        print("Error: 'mnemonic' library not found.  Please install it using 'pip install mnemonic'")
        sys.exit(1)
    return Mnemonic


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Recovers a BIP39 mnemonic phrase from potentially corrupted or partial seeds.")

    # Add arguments for partial or corrupted mnemonic
    parser.add_argument("--partial_mnemonic", type=str, help="The partial or corrupted mnemonic phrase (space-separated).  Use '?' for missing words.", required=False)
    parser.add_argument("--num_missing", type=int, help="Number of missing words in the mnemonic. Use only if --partial_mnemonic has '?' characters", required=False, default=0)
    # There is deliberately no --wordlist_path argument: an earlier one
    # was accepted and silently ignored, which is worse than not offering
    # it. The wordlist always comes from the mnemonic package.
    parser.add_argument("--language", type=str, help="The mnemonic language to use (default: english).", required=False, default="english")
    parser.add_argument("--max_attempts", type=int, help="The maximum number of attempts to generate a valid mnemonic.", required=False, default=10000)
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.", required=False)


    return parser



def generate_all_possible_mnemonics(partial_mnemonic: str, missing_count: int, language: str) -> Iterator[str]:
    """
    Yields possible mnemonics for a partial mnemonic, one at a time.

    This used to build the full list in memory before any validation ran.
    The space is 2048 ** missing_count, so two missing words meant about
    four million strings held at once and three would not fit at all.
    Yielding lets main validate and discard each candidate as it goes;
    the search itself is unchanged, only the holding cost is gone.
    """
    Mnemonic = _load_mnemonic_class()
    mnemo = Mnemonic(language)
    wordlist = mnemo.wordlist
    partial_words = partial_mnemonic.split()
    unknown_indices = [i for i, word in enumerate(partial_words) if word == '?']

    if len(unknown_indices) != missing_count:
        raise ValueError(f"The number of '?' characters ({len(unknown_indices)}) must match the num_missing argument ({missing_count}).")

    current_mnemonic = partial_words[:]

    def generate_recursive(index: int) -> Iterator[str]:
        if index == len(unknown_indices):
            yield " ".join(current_mnemonic)
            return
        unknown_index = unknown_indices[index]
        for word in wordlist:
            current_mnemonic[unknown_index] = word
            yield from generate_recursive(index + 1)

    yield from generate_recursive(0)


def is_valid_mnemonic(mnemonic_phrase: str, language: str) -> bool:
    """
    Validates a BIP39 mnemonic phrase by checking its checksum.

    Args:
        mnemonic_phrase: The mnemonic phrase to validate.
        language: The language of the mnemonic

    Returns:
        True if the mnemonic phrase is valid, False otherwise.
    """

    Mnemonic = _load_mnemonic_class()
    mnemo = Mnemonic(language)
    # check(), not to_seed(): to_seed derives a seed from any string of
    # wordlist words without verifying the checksum, so the old version
    # accepted every completion it generated and the recovery printed
    # thousands of "valid" phrases for one missing word. check() runs
    # the BIP39 checksum and wordlist validation this function promises.
    return mnemo.check(mnemonic_phrase)



def main():
    """
    Main function to parse arguments, recover the mnemonic, and print the results.
    """
    parser = setup_argparse()
    args = parser.parse_args()


    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Debug mode enabled.")



    if not args.partial_mnemonic:
       print("Error: Please provide a partial mnemonic phrase using the --partial_mnemonic argument.")
       sys.exit(1)


    # BIP39 phrases have one of these lengths; anything else can never
    # validate, and saying so up front beats searching a doomed space.
    if len(args.partial_mnemonic.split()) not in (12, 15, 18, 21, 24):
        print("Error: A BIP39 mnemonic has 12, 15, 18, 21 or 24 words.")
        sys.exit(1)

    try:
        valid_mnemonics = []
        attempts = 0
        for mnemonic in generate_all_possible_mnemonics(args.partial_mnemonic, args.num_missing, args.language):
            # --max_attempts existed but was never read, so a run with
            # several missing words had no bound at all. It now caps the
            # number of candidates checked, in generation order.
            if attempts >= args.max_attempts:
                print(f"Stopped after {args.max_attempts} attempts (raise --max_attempts to search further).")
                break
            attempts += 1
            if is_valid_mnemonic(mnemonic, args.language):
                valid_mnemonics.append(mnemonic)


        if valid_mnemonics:
            print("Possible Valid Mnemonic Phrases:")
            for mnemonic in valid_mnemonics:
                print(mnemonic)
        else:
            print("No valid mnemonic phrases could be recovered.")



    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Usage Examples:
#
# 1. Recover a mnemonic with one missing word (12 words total):
#    python main.py --partial_mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ?" --num_missing 1
#
# 2. Recover a mnemonic with two missing words:
#    python main.py --partial_mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ? ?" --num_missing 2 --max_attempts 5000000
#
# 3. Using debug mode to see more details:
#    python main.py --partial_mnemonic="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ?" --num_missing 1 --debug
#
# Notes:
# - The speed of recovery depends heavily on the number of missing words.  Each missing word multiplies the search space by 2048.
# - --max_attempts caps how many candidates are checked (default 10000), so a search with several missing words stops instead of running for days.
