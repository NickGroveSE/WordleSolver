import pandas
import pyautogui
import time
import numpy as np


def readCSV():
    print("Gathering Word Data...")
    reader = pandas.read_csv('./data/wordle.csv')
    return reader.sort_values(by='occurrence', ascending=False)


def main():
    print("Solving...")

    possibleWords = ALL_WORDS["word"].array
    rowsOfPuzzle = locateEmptyRows()
    xCoordinate = rowsOfPuzzle[0].left
    guess = ""
    
    for row in range(0, len(rowsOfPuzzle)):

        currentYCoordinate = rowsOfPuzzle[row].top

        # First Guess is STARE to knockout a lot of common letters
        if row == 0:
            guess = "stare"

        # Guesses 2-6
        else:
            possibleWords = searchForBestGuess(possibleWords)

            # Set Guess to the Top of the Possibilities Array since this Array is sorted by each words Occurrence Probability
            guess = possibleWords[0]

        typeGuess(guess)
        informUser(row, guess)
        time.sleep(3)
        colorAnalysis(xCoordinate, currentYCoordinate, guess)

        if '' not in GREEN_LETTERS:
            print("Correct Guess! " + guess.upper())
            return 
        

def locateEmptyRows():
    return list(pyautogui.locateAllOnScreen('./content/wordle_empty_row.png'))

# Identify Gray, Yellow, and Green Letters Returned from Guess
def colorAnalysis(xCoordinate, currentYCoordinate, guess):
    print("Analyzing Guess Results...")

    # Value Used to Make Sure Our Coordinates are just a little bit in the letter box to identify colors
    colorSeek = 5

    for position in range(0, len(guess)):

        # Check for Greens
        if(pyautogui.pixel(np.int64(xCoordinate+colorSeek).item(), np.int64(currentYCoordinate+colorSeek).item())[1] == 141):

            # Double Letter Gray/Green Check
            if guess[position] in GRAY_LETTERS:
                GRAY_LETTERS.remove(guess[position])

            GREEN_LETTERS[position] = guess[position]

        # Check for Yellows
        elif(pyautogui.pixel(np.int64(xCoordinate+colorSeek).item(), np.int64(currentYCoordinate+colorSeek).item())[1] == 159):

            # No Duplicates Wanted in each Yellow Letters Dict Key
            if guess[position] not in YELLOW_LETTERS[position]:
                YELLOW_LETTERS[position].append(guess[position])

        # Check for Gray Letters
        else:

            # Check for no Duplicates and Double Letter Yellow/Gray Check
            if guess[position] not in GRAY_LETTERS and guess[position] not in guess[:position]:
                GRAY_LETTERS.append(guess[position])

        # Correct Guess Return
        if '' not in GREEN_LETTERS:
            return
        
        # Move X Position to the Right
        xCoordinate = xCoordinate + SQUARE_SIZE


    print(GREEN_LETTERS)  
    print(YELLOW_LETTERS)
    print(GRAY_LETTERS) 


def searchForBestGuess(possibleWords):
    print("Searching For Best Guess...")

    changesToPossible = []

    # Change Possibilities Based On Gray Letters
    for word in possibleWords:
        for letter in GRAY_LETTERS:
            if word in changesToPossible:
                continue
            elif letter in word:
                changesToPossible.append(word)
    possibleWords = possibleWords[~np.in1d(possibleWords,changesToPossible)]
    
    for position in range(0, 5):

        changesToPossible = []

        # Change Possibilities Based on Yellow Letters
        for word in possibleWords:
            if word in changesToPossible:
                continue
            for letter in YELLOW_LETTERS[position]:
                if letter == word[position] or letter not in word:
                    changesToPossible.append(word)
        possibleWords = possibleWords[~np.in1d(possibleWords,changesToPossible)]

        # Change Possibilities Based on Green Letters
        if(GREEN_LETTERS[position] != ''):
                possibleWords = possibleWords[np.in1d(possibleWords, ALL_WORDS["word"].array[[word[position] == GREEN_LETTERS[position] for word in ALL_WORDS["word"]]])] 

    return possibleWords


def typeGuess(guess):
    for letter in guess:
        pyautogui.press(letter)

    pyautogui.press('enter')


def informUser(currentRow, guess):
    print("Guess " + str(currentRow + 1) + ": " + guess.upper())


print("Navigate to the Window Where Wordle is")

# Initialize Letter Containers and Pixel Size of the Letter Squares
YELLOW_LETTERS = {k: [] for k in [0,1,2,3,4]}
GREEN_LETTERS = ['']*5
GRAY_LETTERS = []
SQUARE_SIZE = 67

# Delay Program So The User can Navigate to Wordle
time.sleep(5)

ALL_WORDS = readCSV()
main()
