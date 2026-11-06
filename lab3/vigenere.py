import unicodedata

ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I",
            "Î", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
            "Ș", "T", "Ț", "U", "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)
MIN_KEY_LENGTH = 7

CHAR_MAP = {}
for letter in ALPHABET:
    CHAR_MAP[letter] = letter
    CHAR_MAP[letter.lower()] = letter
CHAR_MAP.update({"Ş": "Ș", "ş": "Ș", "Ţ": "Ț", "ţ": "Ț"})

ALLOWED_TEXT = "letters of the Romanian alphabet (A-Z, a-z, Ă, Â, Î, Ș, Ț, ă, â, î, ș, ț)"


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


def to_numbers(text, alphabet=ALPHABET):
    position = {letter: i for i, letter in enumerate(alphabet)}
    return [position[ch] for ch in text]


def to_letters(numbers, alphabet=ALPHABET):
    return "".join(alphabet[x] for x in numbers)


def extend_key(key, length):
    return (key * (length // len(key) + 1))[:length]


def encrypt(text, key, alphabet=ALPHABET):
    n = len(alphabet)
    m = to_numbers(text, alphabet)
    k = to_numbers(extend_key(key, len(text)), alphabet)
    return to_letters([mod(mi + ki, n) for mi, ki in zip(m, k)], alphabet)


def decrypt(text, key, alphabet=ALPHABET):
    n = len(alphabet)
    c = to_numbers(text, alphabet)
    k = to_numbers(extend_key(key, len(text)), alphabet)
    return to_letters([mod(ci - ki, n) for ci, ki in zip(c, k)], alphabet)


def step_table(text, key, decrypting=False, alphabet=ALPHABET, width=12):
    n = len(alphabet)
    full_key = extend_key(key, len(text))
    x = to_numbers(text, alphabet)
    k = to_numbers(full_key, alphabet)
    sign = -1 if decrypting else 1
    y = [mod(xi + sign * ki, n) for xi, ki in zip(x, k)]
    result = to_letters(y, alphabet)
    names = ("Ciphertext C", "Key K", "C (numbers)", "K (numbers)", f"C-K mod {n}", "Plaintext M") \
        if decrypting else \
        ("Plaintext M", "Key K", "M (numbers)", "K (numbers)", f"M+K mod {n}", "Ciphertext C")
    lines = []
    for start in range(0, len(text), width):
        part = slice(start, start + width)
        rows = [list(text[part]), list(full_key[part]),
                [str(v) for v in x[part]], [str(v) for v in k[part]],
                [str(v) for v in y[part]], list(result[part])]
        for name, cells in zip(names, rows):
            lines.append(f"  {name:<13}" + "".join(f"{c:>4}" for c in cells))
        lines.append("")
    return "\n".join(lines).rstrip()


def read_choice(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"  Error: choose one of: {', '.join(options)}.")


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


def read_key():
    while True:
        raw = input(f"Key (at least {MIN_KEY_LENGTH} Romanian letters, no spaces): ").strip()
        try:
            key = normalize(raw, allow_spaces=False)
        except ValueError as e:
            print(f"  Error: {e}")
            continue
        if len(key) >= MIN_KEY_LENGTH:
            return key
        print(f"  Error: the key has {len(key)} letters; it must have at least {MIN_KEY_LENGTH} "
              f"letters of the Romanian alphabet.")


def show_alphabet():
    print("\nLetter encoding (n = 31):")
    print("  " + " ".join(f"{ch:>2}" for ch in ALPHABET))
    print("  " + " ".join(f"{i:>2}" for i in range(N)))


def main():
    while True:
        print("\n=== Vigenère cipher — Romanian alphabet (n = 31) ===")
        print("1. Encrypt a message")
        print("2. Decrypt a cryptogram")
        print("3. Show the letter encoding")
        print("0. Exit")
        choice = read_choice("Choose: ", ["1", "2", "3", "0"])
        if choice == "0":
            break
        if choice == "3":
            show_alphabet()
            continue

        key = read_key()
        if choice == "1":
            m = read_text("Message: ")
            c = encrypt(m, key)
            print(f"\nKey:                     {key} (length {len(key)})")
            print(f"Message (normalized):    {m}")
            print("\n" + step_table(m, key))
            print(f"\nCryptogram:              {c}")
        else:
            c = read_text("Cryptogram: ")
            m = decrypt(c, key)
            print(f"\nKey:                     {key} (length {len(key)})")
            print(f"Cryptogram (normalized): {c}")
            print("\n" + step_table(c, key, decrypting=True))
            print(f"\nDecrypted message:       {m}")


if __name__ == "__main__":
    main()
