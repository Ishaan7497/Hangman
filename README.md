# 🪢 Hangman

**The classic word-guessing game in your terminal, with three themes and vowel hints.**

[![tests](https://github.com/Ishaan7497/Hangman/actions/workflows/tests.yml/badge.svg)](https://github.com/Ishaan7497/Hangman/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## About

This is a command-line version of the popular Hangman game, where you guess letters to figure out a hidden word before you run out of attempts.

You pick a theme (everyday words, movies or celebrities). Longer answers get a free vowel as a hint, the gallows is drawn in ASCII art as you lose lives, and no word repeats until you've played every word in the theme. It uses only the Python standard library, and a test suite covers the game logic, the menus and the word lists.

## Why I built this

## Features

- **3 themes:** ~850 general words, 50 movies, 85 celebrities
- **Vowel hints:** one vowel is revealed for every 7 letters in the answer
- **5 lives** with an ASCII-art gallows
- **No repeats:** each word is used once before the list starts over
- **Typo-proof input:** invalid letters, repeated guesses and wrong menu answers never cost a life or crash the game

## How to play

```bash
git clone https://github.com/Ishaan7497/Hangman.git
cd Hangman
python hangman.py
```

1. Type `y` to start, then pick a theme (`1`, `2` or `3`).
2. Guess one letter at a time. Spaces in multi-word answers are already filled in.
3. Each wrong letter costs a life. Guess the whole word before all 5 are gone.

```
Guess a letter: a
Correct! The letter is in the word.

__ A __ __
```

## Project structure

```
hangman.py   # game logic and menus
words.py     # word lists for each theme
tests/       # pytest suite
```

To add your own words, append them to a list in `words.py` (letters and spaces only). A test checks that every entry can be guessed.

## Testing

```bash
pip install pytest
pytest
```

Tests run automatically on every push with GitHub Actions.

## License

[MIT](LICENSE)
