import pandas
import pyautogui
import time
import numpy as np

def gatherData():
    print("Gathering Word Data...")
    reader = pandas.read_csv('./data/wordle.csv')
    return reader.sort_values(by='occurrence', ascending=False)


def main():
    print("Solving...")

    possible = data["word"].array
    rows = locateRows()
    x = rows[0].left
    guess = ""
    
    for i in range(0, len(rows)):

        current_y = rows[i].top

        if i == 0:
            guess = "stare"

        else:
            possible = searchForBestGuess(possible)
            guess = possible[0]

        typeGuess(guess)
        informUser(i, guess)
        time.sleep(3)
        colorAnalysis(x, current_y, guess)
        if '' not in green_letters:
            print("Correct Guess! " + guess.upper())
            return 
        

def locateRows():
    return list(pyautogui.locateAllOnScreen('./content/wordle_empty_row.png'))


def colorAnalysis(x, cy, g):
    print("Analyzing Guess Results...")

    color_seek = 5

    for pos in range(0, len(g)):

        if(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 141):
            if g[pos] in gray_letters:
                gray_letters.remove(g[pos])
            green_letters[pos] = g[pos]

        elif(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 159):
            if g[pos] not in yellow_letters[pos]:
                yellow_letters[pos].append(g[pos])

        else:
            if g[pos] not in gray_letters and g[pos] not in g[:pos]:
                gray_letters.append(g[pos])

        if '' not in green_letters:
            return
        x = x + indent


    print(green_letters)  
    print(yellow_letters)
    print(gray_letters) 


def searchForBestGuess(poss):
    print("Searching For Best Guess...")

    changes = []

    for word in poss:
        for letter in gray_letters:
            if word in changes:
                continue
            elif letter in word:
                changes.append(word)

    poss = poss[~np.in1d(poss,changes)]
    
    for pos in range(0, 5):

        changes = []

        for word in poss:
            if word in changes:
                continue
            for letter in yellow_letters[pos]:
                if letter == word[pos] or letter not in word:
                    changes.append(word)

        poss = poss[~np.in1d(poss,changes)]

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
data = pandas.DataFrame()
yellow_letters = {k: [] for k in [0,1,2,3,4]}
green_letters = ['']*5
gray_letters = []
indent = 67
time.sleep(5)
data = gatherData()
main()
