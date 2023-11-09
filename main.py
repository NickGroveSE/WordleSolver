import pandas
import pyautogui
import time
import string
import numpy as np

def gatherData():
    print("Gathering Word Data...")
    return pandas.read_csv('./data/test.csv')

def main():
    print("Solving...")

    rows = locateRows()
    x = rows[0].left
    current_y = rows[0].top
    guess = ""

    # print(pyautogui.pixel(312, 628))
    #width = 67px
    #
    
    for i in range(0, len(rows)):
        if i == 0:
            guess = "ACTED"

        elif i == 1:
            guess = 'FLUBS'

        elif i == 2:
            guess = 'VIGOR'

        elif i == 3:
            guess = 'NYMPH'

        typeGuess(guess)
        informUser(i, guess)
        colorAnalysis(x, current_y, guess)
        current_y = rows[i].top
        time.sleep(4)


def locateRows():
    print("Locating Row...")

    return list(pyautogui.locateAllOnScreen('./content/wordle_empty_row.png'))


def colorAnalysis(x, cy, g):
    print("Analyzing Guess Results...")

    color_seek = 5

    for pos in range(0, len(g)):
        if(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 141):
            green_letters[pos] = g[pos]

        elif(pyautogui.pixel(np.int64(x+color_seek).item(), np.int64(cy+color_seek).item())[1] == 159):
            yellow_letters[g[pos].lower()].append(pos)
                 

        x = x + indent

    print(green_letters)  
    print(yellow_letters) 


# def searchForBestGuess(g):
#     for pos in range(0, 5):
#         if(green_letters[pos] != ''):
#             print(data[data["word"][pos]]== green_letters[pos])


def typeGuess(g):
    for l in g:
        pyautogui.press(l)

    pyautogui.press('enter')


def informUser(gn, g):
    print("Guess " + str(gn + 1) + ": " + g)


print("Navigate to the Window Where Wordle is")
yellow_letters = {k: [] for k in string.ascii_lowercase}
green_letters = ['']*5
indent = 67
time.sleep(5)
data = gatherData()
main()
