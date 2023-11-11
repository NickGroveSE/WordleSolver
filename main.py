import pandas
import pyautogui
import time
import numpy as np

# Reads CSV of Wordle Words
def gatherData():
    print("Gathering Word Data...")
    reader = pandas.read_csv('./data/wordle.csv')
    return reader.sort_values(by='occurrence', ascending=False)


def main():
    print("Solving...")

    # Initialize Possibilities to All Words
    possible = data["word"].array

    # Call Function to Identify The Empty Rows on Screen
    rows = locateRows()
    x = rows[0].left
    guess = ""
    
    for i in range(0, len(rows)):

        current_y = rows[i].top

        # First Guess is STARE to knockout a lot of common letters
        if i == 0:
            guess = "stare"

        # Guesses 2-6
        else:
            possible = searchForBestGuess(possible)

            # Set Guess to the Top of the Possibilities Array since this Array is sorted by each words Occurrence Probability
            guess = possible[0]

        # Guess Word
        typeGuess(guess)
        informUser(i, guess)
        time.sleep(3)

        # Identify Gray, Yellow, and Green Letters Returned from Guess
        colorAnalysis(x, current_y, guess)

        if '' not in green_letters:
            print("Correct Guess! " + guess.upper())
            return 
        

def locateRows():
    return list(pyautogui.locateAllOnScreen('./content/wordle_empty_row.png'))


def colorAnalysis(x, cy, g):
    print("Analyzing Guess Results...")

    # Value Used to Make Sure Our Coordinates are just a little bit in the letter box to identify colors
    color_seek = 5

    # Loop Through Guess Results
    for pos in range(0, len(g)):

        # Check for Greens
        if(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 141):

            # Double Letter Gray/Green Check
            if g[pos] in gray_letters:
                gray_letters.remove(g[pos])

            green_letters[pos] = g[pos]

        # Check for Yellows
        elif(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 159):

            # No Duplicates Wanted in each Yellow Letters Dict Key
            if g[pos] not in yellow_letters[pos]:
                yellow_letters[pos].append(g[pos])

        # Check for Gray Letters
        else:

            # Check for no Duplicates and Double Letter Yellow/Gray Check
            if g[pos] not in gray_letters and g[pos] not in g[:pos]:
                gray_letters.append(g[pos])

        # Correct Guess Return
        if '' not in green_letters:
            return
        
        # Move X Position to the Right
        x = x + indent


    print(green_letters)  
    print(yellow_letters)
    print(gray_letters) 


def searchForBestGuess(poss):
    print("Searching For Best Guess...")

    # Track Words that must be taken out of our Possibilities
    changes = []

    # Change Possibilities Based On Gray Letters
    for word in poss:
        for letter in gray_letters:
            if word in changes:
                continue
            elif letter in word:
                changes.append(word)
    poss = poss[~np.in1d(poss,changes)]
    
    # Loop Through Letter Positions
    for pos in range(0, 5):

        changes = []

        # Change Possibilities Based on Yellow Letters
        for word in poss:
            if word in changes:
                continue
            for letter in yellow_letters[pos]:
                if letter == word[pos] or letter not in word:
                    changes.append(word)
        poss = poss[~np.in1d(poss,changes)]

        # Change Possibilities Based on Green Letters
        if(green_letters[pos] != ''):
                poss = poss[np.in1d(poss, data["word"].array[[word[pos] == green_letters[pos] for word in data["word"]]])] 

    return poss


def typeGuess(g):
    for l in g:
        pyautogui.press(l)

    pyautogui.press('enter')


def informUser(gn, g):
    print("Guess " + str(gn + 1) + ": " + g.upper())


print("Navigate to the Window Where Wordle is")

# Initialize Letter Containers and Pixel Size of the Letter Squares
yellow_letters = {k: [] for k in [0,1,2,3,4]}
green_letters = ['']*5
gray_letters = []
indent = 67

# Delay Program So The User can Navigate to Wordle
time.sleep(5)

data = gatherData()
main()
