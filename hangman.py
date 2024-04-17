from words import word_list, movie_list, famous_people

import random

play = input("Start? (y/n) : ")
if play.lower() == 'y':
    print("Game is starting...\n Welcome to Hangman")
elif play.lower() == 'n':
    print("Exiting game...")
    exit()
else:
    print("Invalid input. Please enter 'y' to start or 'n' to exit.")
    exit()
   

def theme():
    t = input("Choose a theme:\n1) General\n2) Movies\n3) Famous People\n      Enter: ").lower()
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
    vowels = ['a', 'e', 'i', 'o', 'u']
    num = len(w) // 7
    for j in range(num):
        for i in range(len(w)):
            if w[i].lower() in vowels:
                b[i] = w[i]
                break
    return b
    

def play_hangman(x_list, chosen_words):
    x_list = [word for word in x_list if "'" not in word]
    wordy = random.choice(x_list)
    word = wordy.upper()
    chosen_words.sort()
    x_list.sort()
    while wordy in chosen_words:
        wordy = random.choice(x_list)
        if chosen_words == x_list:
            chosen_words = []

    chosen_words.append(wordy)

    blanks = "__ " * len(word)
    blanks = blanks.split()
    for i in range(len(word)):
        if word[i] == " ":
            blanks[i] = " "
    used_letters = []

    new_blanks = vowel(word, blanks)
    lives = 5
    print(f"The word has {new_blanks} letters({len(word) - len(list(filter(lambda x: word[x] == ' ', range(len(word)))))}).\n Guesses: {lives}")

    while lives > 0:
        x = input("Guess a letter: ").upper()
        if lives == 5:
            display_hangman("stage0")
        elif lives == 4:
            display_hangman("stage1")
        elif lives == 3:
            display_hangman("stage2")
        elif lives == 2:
            display_hangman("stage3")
        elif lives == 1:
            display_hangman("stage4")

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
            print("Guesses Left: ", lives)
            used_letters.append(x)
            print("Used words: ", used_letters, "\n")

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
            break


chosen_words1 = []
chosen_words2 = []
chosen_words3 = []
while True:

    if selected_theme == '1':

        play_hangman(word_list, chosen_words1)
        play_again()

    elif selected_theme == "2":

        play_hangman(movie_list, chosen_words2)
        play_again()

    elif selected_theme == '3':
        play_hangman(famous_people, chosen_words3)
        play_again()
    
    
    else:
     print("Invalid theme. Pick general, movies or famous people.")
     selected_theme = theme()
    