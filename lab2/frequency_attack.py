import sys
from collections import Counter
from pathlib import Path

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ENGLISH_FREQ = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23, "G": 2.01,
    "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75,
    "O": 7.51, "P": 1.93, "Q": 0.09, "R": 5.99, "S": 6.33, "T": 9.06, "U": 2.76,
    "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07,
}

ATTACK_STEPS = [
    ("V=e W=t",
     "V (11.04%) and W (10.11%) are the two most frequent letters of the cryptogram, "
     "and E (12.70%) and T (9.06%) are the two most frequent letters of English."),
    ("Q=h",
     "The three-letter word tQe is the most frequent word of the text; "
     "the most common English word is 'the'."),
    ("T=a",
     "T is a word on its own 12 times ('of T game', 'T puzzle'); P is alone only after "
     "an apostrophe ('s). In English only 'a' and 'I' are one-letter words, and T is frequent (7.48%)."),
    ("G=n O=d",
     "aGO is the most frequent three-letter word after the; "
     "a three-letter word that starts with 'a' and is that common is 'and'."),
    ("X=i",
     "The two-letter words Xn and Xt are very common: they can only be 'in' and 'it'."),
    ("N=o C=f",
     "tN and NC are frequent two-letter words: 'to' and 'of'. "
     "N is also the 4th most frequent letter, close to O in English."),
    ("P=s",
     "The words thePe and iP become 'these' and 'is'."),
    ("I=r",
     "foI and shoItest are clearly 'for' and 'shortest'."),
    ("R=w",
     "Ras and Rhen become 'was' and 'when'."),
    ("H=c F=y",
     "The word seHreHF can only be 'secrecy'."),
    ("U=p S=l J=g",
     "cryUtoSoJy is 'cryptology', a word that appears many times in the text."),
    ("Z=m A=b D=u",
     "Zore, Aorn and sDch become 'more', 'born' and 'such'."),
    ("K=v L=k M=z",
     "haKe, Lnown and puMMle become 'have', 'known' and 'puzzle'."),
    ("B=q E=j Y=x",
     "Buasi, Eust and neYt become 'quasi', 'just' and 'next'; "
     "these are the rarest letters, as in English."),
]


def load_ciphertext(path):
    return Path(path).read_text(encoding="utf-8").strip()


def letter_counts(text):
    return Counter(ch for ch in text.upper() if ch in LETTERS)


def frequency_table(text):
    counts = letter_counts(text)
    total = sum(counts.values())
    rows = [(letter, counts[letter], 100 * counts[letter] / total) for letter in LETTERS]
    return rows, total


def words(text):
    cleaned = "".join(ch if ch in LETTERS else " " for ch in text.upper())
    return cleaned.split()


def ngram_counts(text, n):
    grams = Counter()
    for word in words(text):
        for i in range(len(word) - n + 1):
            grams[word[i:i + n]] += 1
    return grams


def doubled_letters(text):
    pairs = Counter()
    for word in words(text):
        for a, b in zip(word, word[1:]):
            if a == b:
                pairs[a + b] += 1
    return pairs


def short_words(text, length):
    return Counter(w for w in words(text) if len(w) == length)


def apply_key(text, key):
    result = []
    for ch in text.upper():
        result.append(key[ch].lower() if ch in key else ch)
    return "".join(result)


def decrypt_final(text, key):
    result = []
    for ch in text:
        up = ch.upper()
        if up in key:
            plain = key[up]
            result.append(plain.upper() if ch.isupper() else plain)
        else:
            result.append(ch)
    return "".join(result)


def parse_substitutions(line):
    pairs = []
    for item in line.replace(",", " ").split():
        if len(item) != 3 or item[1] != "=":
            raise ValueError(f"'{item}' is not in the form X=e (cipher letter = plain letter).")
        cipher, plain = item[0].upper(), item[2].lower()
        if cipher not in LETTERS or plain.upper() not in LETTERS:
            raise ValueError(f"'{item}' must use letters A-Z only.")
        pairs.append((cipher, plain))
    if not pairs:
        raise ValueError("Enter at least one substitution, for example V=e.")
    return pairs


def add_substitutions(key, pairs):
    new_key = dict(key)
    for cipher, plain in pairs:
        for other, used in new_key.items():
            if used == plain and other != cipher:
                raise ValueError(f"The plain letter '{plain}' is already the image of {other}. "
                                 f"Two cipher letters cannot decrypt to the same letter.")
        new_key[cipher] = plain
    return new_key


def print_frequencies(text):
    rows, total = frequency_table(text)
    ordered = sorted(rows, key=lambda r: -r[1])
    english = sorted(ENGLISH_FREQ.items(), key=lambda r: -r[1])
    print(f"\nLetters in the cryptogram: {total}")
    print(f"  {'Cipher':>6} {'Count':>6} {'%':>7}   {'English':>7} {'%':>6}   Chart")
    for (letter, count, pct), (en_letter, en_pct) in zip(ordered, english):
        bar = "#" * round(pct * 2)
        print(f"  {letter:>6} {count:>6} {pct:>7.2f}   {en_letter:>7} {en_pct:>6.2f}   {bar}")


def print_patterns(text):
    def show(title, counter, top=12):
        items = ", ".join(f"{k} {v}" for k, v in counter.most_common(top))
        print(f"  {title}: {items}")
    print()
    show("Bigrams", ngram_counts(text, 2))
    show("Trigrams", ngram_counts(text, 3))
    show("Doubled letters", doubled_letters(text), 8)
    show("1-letter words", short_words(text, 1), 5)
    show("2-letter words", short_words(text, 2), 10)
    show("3-letter words", short_words(text, 3), 10)


def print_key(key):
    print("\nCipher: " + " ".join(LETTERS))
    print("Plain:  " + " ".join(key.get(c, ".") for c in LETTERS))
    inverse = {plain.upper(): cipher for cipher, plain in key.items()}
    plain_letters = [c.lower() for c in LETTERS]
    print("\nPlain:  " + " ".join(plain_letters))
    print("Cipher: " + " ".join(inverse.get(c, ".") for c in LETTERS))
    print(f"\nKnown letters: {len(key)} of 26")


def print_text(text, key, lines=None):
    shown = apply_key(text, key).split("\n")
    if lines:
        shown = shown[:lines]
    print()
    print("\n".join(shown))


def frequency_order_guess(text):
    counts = letter_counts(text)
    cipher_order = [l for l, _ in counts.most_common()]
    english_order = [l for l, _ in sorted(ENGLISH_FREQ.items(), key=lambda r: -r[1])]
    return {c: p.lower() for c, p in zip(cipher_order, english_order)}


def replay_attack(text, preview_lines):
    key = {}
    for number, (subs, reason) in enumerate(ATTACK_STEPS, 1):
        key = add_substitutions(key, parse_substitutions(subs))
        print(f"\n--- Step {number}: {subs} ---")
        print(f"Reason: {reason}")
        print_text(text, key, preview_lines)
        if sys.stdin.isatty():
            input("\n(Enter for the next step)")
    print("\n=== Decrypted message ===\n")
    print(decrypt_final(text, key))
    print_key(key)
    return key


def read_line(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return "0"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("ciphertext_v2.txt")
    text = load_ciphertext(path)
    key = {}
    history = []

    while True:
        print("\n=== Frequency analysis attack on a monoalphabetic cipher ===")
        print("1. Letter frequencies (compared with English)")
        print("2. Bigrams, trigrams, doubled letters and short words")
        print("3. Add substitutions (for example: V=e W=t)")
        print("4. Undo the last step")
        print("5. Show the text with the current substitutions")
        print("6. Show the reconstructed key")
        print("7. Guess by frequency order only")
        print("8. Replay the full attack step by step")
        print("9. Show the decrypted message")
        print("0. Exit")
        choice = read_line("Choose: ")

        if choice == "0":
            break
        elif choice == "1":
            print_frequencies(text)
        elif choice == "2":
            print_patterns(text)
        elif choice == "3":
            line = read_line("Substitutions: ")
            try:
                new_key = add_substitutions(key, parse_substitutions(line))
            except ValueError as e:
                print(f"  Error: {e}")
                continue
            history.append(key)
            key = new_key
            print_text(text, key, 6)
        elif choice == "4":
            if history:
                key = history.pop()
                print("  The last step was undone.")
            else:
                print("  Error: there is nothing to undo.")
        elif choice == "5":
            print_text(text, key)
        elif choice == "6":
            print_key(key)
        elif choice == "7":
            print_text(text, frequency_order_guess(text), 6)
        elif choice == "8":
            history.append(key)
            key = replay_attack(text, 6)
        elif choice == "9":
            if len(key) < 26:
                print(f"  Only {len(key)} of 26 letters are known; unknown letters stay in uppercase.")
                print_text(text, key)
            else:
                print()
                print(decrypt_final(text, key))
        else:
            print("  Error: choose a number from 0 to 9.")


if __name__ == "__main__":
    main()
