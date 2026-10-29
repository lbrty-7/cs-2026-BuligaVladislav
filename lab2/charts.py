from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from frequency_attack import ENGLISH_FREQ, LETTERS, frequency_table, load_ciphertext

BAR = "#2a78d6"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
HERE = Path(__file__).parent
OUT = HERE / "figures"


def style(ax, title, ymax):
    ax.set_title(title, loc="left", fontsize=12, color=INK, pad=10)
    ax.set_ylim(0, ymax)
    ax.set_ylabel("Frequency, %", color=INK_2, fontsize=10)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK_2)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)


def bars(ax, labels, values, highlight=5):
    ax.bar(labels, values, color=BAR, width=0.7, edgecolor="white", linewidth=1)
    top = sorted(range(len(values)), key=lambda i: -values[i])[:highlight]
    for i in top:
        ax.text(i, values[i] + 0.25, f"{values[i]:.2f}", ha="center", fontsize=8, color=INK_2)


def main():
    OUT.mkdir(exist_ok=True)
    text = load_ciphertext(HERE / "ciphertext_v2.txt")
    rows, _ = frequency_table(text)
    cipher = {letter: pct for letter, _, pct in rows}
    ymax = 14

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
    bars(axes[0], list(LETTERS), [ENGLISH_FREQ[l] for l in LETTERS])
    style(axes[0], "Letter frequency in English", ymax)
    bars(axes[1], list(LETTERS), [cipher[l] for l in LETTERS])
    style(axes[1], "Letter frequency in the cryptogram (V2)", ymax)
    axes[1].set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "freq_alphabetical.png", dpi=200, facecolor="white")

    eng_sorted = sorted(ENGLISH_FREQ.items(), key=lambda r: -r[1])
    cip_sorted = sorted(cipher.items(), key=lambda r: -r[1])
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.2), sharey=True)
    bars(axes[0], [l for l, _ in eng_sorted], [v for _, v in eng_sorted])
    style(axes[0], "English, in decreasing order", ymax)
    bars(axes[1], [l for l, _ in cip_sorted], [v for _, v in cip_sorted])
    style(axes[1], "Cryptogram (V2), in decreasing order", ymax)
    axes[1].set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "freq_sorted.png", dpi=200, facecolor="white")
    print(f"Charts saved in {OUT}")


if __name__ == "__main__":
    main()
