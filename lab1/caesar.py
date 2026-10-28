import unicodedata

ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I",
            "Î", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
            "Ș", "T", "Ț", "U", "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)

CHAR_MAP = {}
for letter in ALPHABET:
    CHAR_MAP[letter] = letter
    CHAR_MAP[letter.lower()] = letter
CHAR_MAP.update({"Ş": "Ș", "ş": "Ș", "Ţ": "Ț", "ţ": "Ț"})

ALLOWED_TEXT = "letters of the Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț), upper- or lowercase"


def normalize(text, allow_spaces=True):
    text = unicodedata.normalize("NFC", text)
    result = []
    for ch in text:
        if ch == " " and allow_spaces:
            continue
        if ch not in CHAR_MAP:
            shown = "space" if ch == " " else repr(ch)
            allowed = ALLOWED_TEXT + (" and spaces" if allow_spaces else "")
            raise ValueError(f"Invalid character {shown}. Allowed: {allowed}.")
        result.append(CHAR_MAP[ch])
    return "".join(result)


def mod(a, n):
    r = a % n
    return r + n if r < 0 else r


def encrypt(text, k, alphabet=ALPHABET):
    n = len(alphabet)
    position = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[mod(position[ch] + k, n)] for ch in text)


def decrypt(text, k, alphabet=ALPHABET):
    n = len(alphabet)
    position = {letter: i for i, letter in enumerate(alphabet)}
    return "".join(alphabet[mod(position[ch] - k, n)] for ch in text)


def build_permuted_alphabet(keyword, alphabet=ALPHABET):
    permuted = []
    for ch in list(keyword) + alphabet:
        if ch not in permuted:
            permuted.append(ch)
    return permuted


def read_key():
    while True:
        raw = input("Key 1 (shift, integer from 1 to 30): ").strip()
        try:
            k = int(raw)
        except ValueError:
            print(f"  Error: '{raw}' is not an integer. The key must be an integer from 1 to {N - 1}.")
            continue
        if 1 <= k <= N - 1:
            return k
        print(f"  Error: {k} is out of range. The key must be an integer from 1 to {N - 1}.")


def read_text(prompt):
    while True:
        try:
            text = normalize(input(prompt))
        except ValueError as e:
            print(f"  Error: {e}")
            continue
        if text:
            return text
        print("  Error: the text is empty. Enter at least one letter.")


def read_keyword():
    while True:
        raw = input("Key 2 (keyword, at least 7 Romanian letters, no spaces): ").strip()
        try:
            keyword = normalize(raw, allow_spaces=False)
        except ValueError as e:
            print(f"  Error: {e}")
            continue
        if len(keyword) >= 7:
            return keyword
        print(f"  Error: the keyword has {len(keyword)} letters; it must have at least 7 "
              f"letters of the Romanian alphabet.")


def read_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"  Error: choose one of: {', '.join(options)}.")


def show_alphabet(alphabet, title):
    print(f"\n{title}:")
    print("  " + " ".join(f"{i:>2}" for i in range(len(alphabet))))
    print("  " + " ".join(f"{ch:>2}" for ch in alphabet))


def main():
    while True:
        print("\n=== Caesar cipher — Romanian alphabet (n = 31) ===")
        print("1. Task 1.1 — Caesar cipher (one key)")
        print("2. Task 1.2 — Caesar cipher with permutation (two keys)")
        print("0. Exit")
        task = read_choice("Choose: ", ["1", "2", "0"])
        if task == "0":
            break

        op = read_choice("Operation — (e)ncrypt or (d)ecrypt: ", ["e", "d"])
        k = read_key()

        alphabet = ALPHABET
        if task == "2":
            keyword = read_keyword()
            alphabet = build_permuted_alphabet(keyword)
            show_alphabet(ALPHABET, "Original alphabet")
            show_alphabet(alphabet, f"Permuted alphabet (keyword {keyword})")

        if op == "e":
            m = read_text("Message: ")
            print(f"\nPlaintext (normalized): {m}")
            print(f"Ciphertext:             {encrypt(m, k, alphabet)}")
        else:
            c = read_text("Ciphertext: ")
            print(f"\nCiphertext (normalized): {c}")
            print(f"Decrypted message:       {decrypt(c, k, alphabet)}")


if __name__ == "__main__":
    main()
