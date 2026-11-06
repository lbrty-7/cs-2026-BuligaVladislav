import random

from vigenere import ALPHABET, decrypt, encrypt, normalize

ENGLISH = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def test_example_from_the_laboratory_work():
    c = encrypt("PERASPERAADASTRA", "SUPER", ENGLISH)
    assert c == "HYGEJHYGERVUHXIS"
    assert decrypt(c, "SUPER", ENGLISH) == "PERASPERAADASTRA"


def test_romanian_example():
    m = normalize("Criptografia este ştiinţa secretelor")
    k = normalize("securitate", allow_spaces=False)
    assert m == "CRIPTOGRAFIAESTEȘTIINȚASECRETELOR"
    c = encrypt(m, k)
    assert c == "UVLJJWARTKAEIMJNLTÂNEZCMVLJEMJCTȚ"
    assert decrypt(c, k) == m


def test_wrap_around():
    assert encrypt("Z", "ĂĂĂĂĂĂĂ") == "A"
    assert decrypt("A", "ĂĂĂĂĂĂĂ") == "Z"


def test_random_round_trips():
    rng = random.Random(1)
    for _ in range(1000):
        m = "".join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 60)))
        k = "".join(rng.choice(ALPHABET) for _ in range(rng.randint(7, 15)))
        assert decrypt(encrypt(m, k), k) == m


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print(f"{name}: passed")
