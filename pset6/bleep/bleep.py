import sys
from cs50 import get_string
from sys import argv


def main():
    #Check the directory
    txtDirc = ipCheck(argv)
    if txtDirc == 1:
        return 1
    #Read the file
    bannedWords = open(txtDirc, 'r')
    wordsList=[]
    for word in bannedWords:
        wordsList.append(word.split('\n')[0])
    #Ask for an input
    txtList = get_string("What message would you like to censor?\n").split(" ")
    #Check for banned words
    for i in range(len(txtList)):
        if txtList[i].lower() in wordsList:
            txtList[i] = "*" * len(txtList[i])
    print(" ".join(txtList))


def ipCheck(argv):
    if len(argv) != 2:
        print("Usage: python bleep.py bannedWords Directory")
        return 1
    return argv[1]

if __name__ == "__main__":
    sys.exit(main())
