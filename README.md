# Cryptography and Security – Laboratory Works

**Student:** Buliga Vladislav, group FAF-243  
**Course:** Cryptography and Security, FCIM / FAF, UTM, 2026–2027  
**Checked by:** Zaica Maia, asist. univ.

Each laboratory work is on its own branch (`lab1`, `lab2`, ...); `main` has all of them, one folder per lab.

| Branch / folder | Laboratory work | Contents |
|---|---|---|
| `lab1` | Lab 1 – The Caesar Cipher and the Caesar Cipher with a Permutation (Romanian alphabet, n = 31) | report (.docx + .md), screenshots, Python program |
| `lab2` | Lab 2 – Cryptanalysis of Monoalphabetic Ciphers (frequency analysis attack, variant 2) | report (.docx + .md), charts, screenshots, Python program, cryptogram |
| `lab3` | Lab 3 – Polyalphabetic Ciphers: the Vigenère cipher for the Romanian alphabet (task 3.2) | report (.docx + .md), screenshots, Python program, tests |

## Running a lab

Requires Python 3, no extra packages (the Lab 2 charts also need `matplotlib`).

```bash
cd lab1
python3 caesar.py

cd lab2
python3 frequency_attack.py
python3 charts.py          # optional, redraws the charts

cd lab3
python3 vigenere.py
python3 test_vigenere.py   # optional, runs the tests
```
