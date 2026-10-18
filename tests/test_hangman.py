import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import hangman  # noqa: E402
from words import famous_people, movie_list, word_list  # noqa: E402


def feed(monkeypatch, *answers):
    """Make input() return these answers in order (fails if more are needed)."""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def pick(monkeypatch, word):
    """Make the game choose `word`."""
    monkeypatch.setattr(hangman.random, "choice", lambda seq: word)


# ── vowel hints ──────────────────────────────────────────────────────────────

def blanks_for(word):
    return ["__" if c != " " else " " for c in word]


@pytest.mark.parametrize("word,expected", [
    ("CAT", 0), ("ORANGE", 0), ("BALANCE", 1), ("ADVERTISEMENT", 1),
    ("ABCDEFGHIJKLMN", 2), ("THE GODFATHER", 1), ("THE LORD OF THE RINGS", 2),
])
def test_one_vowel_revealed_per_seven_letters_ignoring_spaces(word, expected):
    b = blanks_for(word)
    assert hangman.vowel(word, b) == expected
    assert sum(1 for x in b if x not in ("__", " ")) == expected


def test_each_hint_reveals_a_different_position():
    word = "AAAAAAAAAAAAAA"          # 14 letters -> 2 hints
    b = blanks_for(word)
    hangman.vowel(word, b)
    assert b[:2] == ["A", "A"] and b[2:] == ["__"] * 12


def test_word_with_no_vowels_gets_no_hint():
    b = blanks_for("RHYTHMS")
    assert hangman.vowel("RHYTHMS", b) == 0
    assert b == ["__"] * 7


def test_hints_never_overwrite_spaces():
    word = "A B C D E F G H"
    b = blanks_for(word)
    hangman.vowel(word, b)
    assert all(b[i] == " " for i, c in enumerate(word) if c == " ")


# ── a single game ────────────────────────────────────────────────────────────

def test_guessing_every_letter_wins(monkeypatch, capsys):
    pick(monkeypatch, "Cars")
    feed(monkeypatch, "c", "a", "r", "s")
    hangman.play_hangman(["Cars"], [])
    assert "You win! The correct word is: CARS" in capsys.readouterr().out


def test_five_wrong_guesses_lose(monkeypatch, capsys):
    pick(monkeypatch, "Cars")
    feed(monkeypatch, "z", "x", "q", "w", "v")     # exactly 5, no more asked
    hangman.play_hangman(["Cars"], [])
    out = capsys.readouterr().out
    assert "You ran out of guesses. The word is: CARS" in out
    assert "X-X" in out                             # final gallows drawn


@pytest.mark.parametrize("bad", ["", " ", "ab", "1", "?", "c4"])
def test_invalid_guesses_cost_no_lives(monkeypatch, capsys, bad):
    pick(monkeypatch, "Ted")
    feed(monkeypatch, bad, bad, bad, bad, bad, bad, "t", "e", "d")
    hangman.play_hangman(["Ted"], [])
    out = capsys.readouterr().out
    assert "You win!" in out
    assert "Please enter a singular letter" in out


def test_repeated_letter_costs_no_life(monkeypatch, capsys):
    pick(monkeypatch, "Ted")
    feed(monkeypatch, "z", "z", "z", "z", "z", "z", "t", "e", "d")
    hangman.play_hangman(["Ted"], [])
    out = capsys.readouterr().out
    assert "You win!" in out
    assert out.count("already been guessed") == 5


def test_multi_word_answers_only_need_letters(monkeypatch, capsys):
    pick(monkeypatch, "Top Gun")
    feed(monkeypatch, "t", "o", "p", "g", "u", "n")
    hangman.play_hangman(["Top Gun"], [])
    assert "You win! The correct word is: TOP GUN" in capsys.readouterr().out


def test_guessing_a_hinted_vowel_still_counts(monkeypatch, capsys):
    pick(monkeypatch, "Balance")                    # 7 letters: first A is shown
    feed(monkeypatch, "a", "b", "l", "n", "c", "e")
    hangman.play_hangman(["Balance"], [])
    assert "You win!" in capsys.readouterr().out


def test_gallows_tracks_lives(monkeypatch, capsys):
    pick(monkeypatch, "Ted")
    feed(monkeypatch, "z", "t", "e", "d")
    hangman.play_hangman(["Ted"], [])
    out = capsys.readouterr().out
    assert "Guesses Left:  4" in out
    assert out.count("O\n") >= 1                   # head drawn after 1 miss


# ── no repeated words ────────────────────────────────────────────────────────

def lose_quickly(monkeypatch):
    # words below only use letters a-e, so these always miss
    answers = iter(["z", "y", "x", "w", "v"] * 100)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))


def test_no_word_repeats_until_all_used(monkeypatch, capsys):
    words = ["ab", "cd", "bead", "dab", "cab"]
    chosen = []
    lose_quickly(monkeypatch)
    for _ in range(len(words)):
        hangman.play_hangman(words, chosen)
    assert sorted(chosen) == sorted(words)
    hangman.play_hangman(words, chosen)              # all used -> starts over
    assert len(chosen) == 1


# ── menus ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("answer,expected", [
    ("1", "General"), ("general", "General"), ("2", "Movies"), ("MOVIES", "Movies"),
    (" 3 ", "Celebrities"), ("celebrities", "Celebrities"),
])
def test_theme_choice(monkeypatch, answer, expected):
    feed(monkeypatch, answer)
    assert hangman.theme() == expected


def test_invalid_theme_asks_again(monkeypatch, capsys):
    feed(monkeypatch, "4", "", "sports", "2")
    assert hangman.theme() == "Movies"
    assert capsys.readouterr().out.count("Invalid theme") == 3


@pytest.mark.parametrize("answer,expected", [("y", True), ("YES", True), (" n ", False), ("no", False)])
def test_yes_no(monkeypatch, answer, expected):
    feed(monkeypatch, answer)
    assert hangman.ask_yes_no("> ") is expected


def test_invalid_play_again_answer_asks_again(monkeypatch):
    feed(monkeypatch, "maybe", "", "n")
    assert hangman.play_again() is False


def test_saying_no_at_start_exits(monkeypatch, capsys):
    feed(monkeypatch, "n")
    hangman.main()
    assert "Exiting game..." in capsys.readouterr().out


def test_full_session(monkeypatch, capsys):
    pick(monkeypatch, "Cars")
    feed(monkeypatch, "y", "2", "c", "a", "r", "s", "y", "c", "a", "r", "s", "n")
    hangman.main()
    out = capsys.readouterr().out
    assert out.count("You win!") == 2
    assert out.rstrip().endswith("Exiting...")


@pytest.mark.parametrize("stdin", ["", "y\n", "y\n1\n"])
def test_running_out_of_input_exits_cleanly(stdin):
    r = subprocess.run([sys.executable, "hangman.py"], input=stdin, cwd=ROOT,
                       capture_output=True, text=True, timeout=10)
    assert r.returncode == 0
    assert "Traceback" not in r.stderr
    assert "Exiting..." in r.stdout


# ── word lists ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("name,words", [
    ("word_list", word_list), ("movie_list", movie_list), ("famous_people", famous_people),
])
def test_word_lists_are_clean_and_winnable(name, words):
    assert words, f"{name} is empty"
    assert len(words) == len(set(words)), f"{name} has duplicates"
    for w in words:
        assert w == w.strip(), f"{w!r} has extra spaces"
        assert re.fullmatch(r"[A-Za-z]+( [A-Za-z]+)*", w), f"{w!r} can't be guessed letter by letter"
