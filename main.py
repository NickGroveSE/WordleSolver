import pandas
import pyautogui
import time
import string
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
            guess = "lucky"

        else:
            possible = searchForBestGuess(possible)
            guess = possible[0]

        typeGuess(guess)
        informUser(i, guess)
        time.sleep(3)
        colorAnalysis(x, current_y, guess) 
        


def locateRows():
    print("Locating Row...")

    return list(pyautogui.locateAllOnScreen('./content/wordle_empty_row.png'))


def colorAnalysis(x, cy, g):
    print("Analyzing Guess Results...")

    color_seek = 5

    for pos in range(0, len(g)):
        # print(x)
        # print(cy)
        # print(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item()))

        if(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 141):
            print("Green Found: " + g[pos].upper())
            green_letters[pos] = g[pos]

        elif(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 159):
            if g[pos] not in yellow_letters[pos]:
                print("Yellow Found: " + g[pos].upper())
                yellow_letters[pos].append(g[pos])

        else:
            if g[pos] not in gray_letters:
                print("Gray Found: " + g[pos].upper())
                if g[pos] in g[:pos] and g[pos] not in gray_letters:
                    yellow_letters[pos].append(g[pos])
                else:
                    gray_letters.append(g[pos])
                 

        x = x + indent

    print(green_letters)  
    print(yellow_letters) 


def searchForBestGuess(poss):

    # print(poss[[letter in word for letter in gray_letters for word in poss]])
    # poss = poss[[]]
    # print(poss)
    changes = []

    for word in poss:
        for letter in gray_letters:
            if word in changes:
                continue
            elif letter in word:
                changes.append(word)

    poss = poss[~np.in1d(poss,changes)]
    # print(poss) 
    

    for pos in range(0, 5):
        # poss = poss[~np.in1d(poss, data["word"].array[[word[pos].lower() not in gray_letters for word in data["word"]]])]
        # print(gray_letters)
        
        
        # print(~np.in1d(poss, data["word"].array[[word[pos].lower() not in gray_letters for word in data["word"]]]))

        changes = []

        for word in poss:
            if word in changes:
                continue
            for letter in yellow_letters[pos]:
                if letter == word[pos] or letter not in word:
                    changes.append(word)

        poss = poss[~np.in1d(poss,changes)]
        # print(poss) 

        if(green_letters[pos] != ''):
                poss = poss[np.in1d(poss, data["word"].array[[word[pos] == green_letters[pos] for word in data["word"]]])]
                # print(poss)    

    return poss


def typeGuess(g):
    for l in g:
        pyautogui.press(l)

    pyautogui.press('enter')


def informUser(gn, g):
    print("Guess " + str(gn + 1) + ": " + g)


print("Navigate to the Window Where Wordle is")
data = pandas.DataFrame()
yellow_letters = {k: [] for k in [0,1,2,3,4]}
green_letters = ['']*5
gray_letters = []
indent = 67
time.sleep(5)
data = gatherData()
main()
