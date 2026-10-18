from words import word_list, movie_list, famous_people

import random

play = input("Start? (y/n) : ")
if play.lower() == 'y':
    print("Game is starting...\nWelcome to Hangman")
elif play.lower() == 'n':
    print("Exiting game...")
    exit()
else:
    print("Invalid input. Please enter 'y' to start or 'n' to exit.")
    exit()
   

def theme():
    t = input("\nChoose a theme:\n1) General\n2) Movies\n3) Celebrities\n\nEnter: ").lower()
    if t == '1' or t == 'general':
        t = "General"
    elif t == '2' or t == 'movies':
        t = "Movies"
    else:
        t = "Celebrities"
    print("Theme chosen:", t)
    return t

selected_theme = theme()



def display_hangman(stage):
    stage0 = """
                - - - - - - - - \\
                |    /           |
                |   /            |
                |  /              
                | /               
                |                
                |
                |       
             -------   
                                """

    stage1 = """
                - - - - - - - - \\
                |    /           |
                |   /            |
                |  /             O
                | /               
                |                
                |
                |       
             -------   
                                """
    stage2 = """
                - - - - - - - - \\
                |    /          |
                |   /           |
                |  /            O
                | /             |
                |                
                |
                |       
             -------   
                                """
    stage3 = """
                - - - - - - - - \\
                |    /          |
                |   /           |
                |  /            O
                | /            \|
                |                
                |
                |       
             -------   
                                """
    stage4 = """
                - - - - - - - - \\
                |    /          |
                |   /           |
                |  /            O
                | /            \|/
                |              /
                |
                |       
             -------   
                                """
    stage5 = """
                - - - - - - - - \\
                |    /          |
                |   /           |
                |  /           X-X
                | /            \|/
                |              / \\
                |                 
                |       
             -------   
                                """
    if stage == "stage0":
        print(stage0)
    elif stage == "stage1":
        print(stage1)
    elif stage == "stage2":
        print(stage2)
    elif stage == "stage3":
        print(stage3)
    elif stage == "stage4":
        print(stage4)
    elif stage == "stage5":
        print(stage5)


def vowel(w, b):
    """Reveal one vowel in `b` for every 7 letters in `w` (spaces don't count).

    Returns how many vowels were revealed."""
    vowels = ['a', 'e', 'i', 'o', 'u']
    num = (len(w) - w.count(" ")) // 7
    shown = 0
    for i in range(len(w)):
        if shown == num:
            break
        if w[i].lower() in vowels and b[i] == "__":
            b[i] = w[i]
            shown += 1
    return shown
    

def play_hangman(x_list, chosen_words):
    x_list = [word.strip() for word in x_list if "'" not in word]
    # Don't repeat a word until every word in the theme has been played.
    remaining = [w for w in x_list if w not in chosen_words]
    if not remaining:
        chosen_words.clear()
        remaining = x_list
    wordy = random.choice(remaining)
    word = wordy.upper()
    chosen_words.append(wordy)
    
    blanks = "__ " * len(word)
    blanks = blanks.split()
    for i in range(len(word)):
        if word[i] == " ":
            blanks[i] = ' '
    used_letters = []
   
    revealed = vowel(word, blanks)
    lives = 5
    msg = "BEEN DISPLAYED (Vowel may have more than one occurence in the word)."

    print(f"\nThe word has {' '.join(blanks)} letters({len(word) - word.count(' ')}).\n Guesses: {lives}")
    if revealed == 1:
        print(f"1 VOWEL HAS {msg}")
    elif revealed > 1:
        print(f"{revealed} VOWELS HAVE {msg}")


    
    display_hangman("stage0")
    while lives > 0:
        x = input("Guess a letter: ").upper()

        if len(x) != 1 or not x.isalpha():
            print("Please enter a singular letter.\n")
        elif x in used_letters:
            print("Letter has already been guessed, try again.\n")
        elif x in word:
            print("Correct! The letter is in the word.\n")

            used_letters.append(x)
            for i in range(len(word)):
                if word[i] == x:
                    blanks[i] = x
            print(" ".join(blanks))
            if "__" not in blanks:
                print("You win! The correct word is:", word.upper())
                return True

        else:
            print("Incorrect. The letter is not in the word.")
            lives -= 1
            if lives > 0:
                display_hangman(f"stage{5 - lives}")
            print("Guesses Left: ", lives)
            used_letters.append(x)
            print("Used letters: ", used_letters, "\n")

    print("You ran out of guesses. The word is:", word)
    display_hangman("stage5")
    return True


def play_again():
    while True:
        p = input("Play again? (y/n): ").lower()
        if p == "y":
            return True
        elif p == 'n':
            print("Exiting...")
            quit()
        else:
            print("Please type in 'y' to play again or 'n' to quit.")


chosen_words1 = []
chosen_words2 = []
chosen_words3 = []
while True:

    if selected_theme == 'General':

        play_hangman(word_list, chosen_words1)
        play_again()

    elif selected_theme == "Movies":

        play_hangman(movie_list, chosen_words2)
        play_again()

    elif selected_theme == 'Celebrities':
        play_hangman(famous_people, chosen_words3)
        play_again()
    
    
    else:
     print("Invalid theme. Pick general, movies or famous people.")
     selected_theme = theme()
    