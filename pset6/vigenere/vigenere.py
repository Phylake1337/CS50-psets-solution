import sys
from sys import argv
from cs50 import get_string

def main():
    #Check key
    if len(argv) != 2:
        print("Usage: ./vigenere key")
        return 1

    for char in argv[1]:
        if not char.isalpha():
            print("Usage: ./vigenere key should be letters")
            return 1

    key = argv[1]
    #Ask for the input
    plaintxt = get_string("Write plaintxt: ")
    #getting the shift key
    shiftKey = getShiftKey(key)
    #Ciphering
    Cipher(shiftKey, plaintxt)

def Cipher(shiftKey, plaintxt):
    ciphertxt = ""
    c = 0
    for i in range(len(plaintxt)):
        #handle non-char
        if not plaintxt[i].isalpha():
            ciphertxt += (plaintxt[i])
            c += 1
            continue
        key = shiftKey[(i - c) % (len(shiftKey))]
        if plaintxt[i].isupper():
            ciphertxt += chr((((ord(plaintxt[i]) - 65) + key) % 26) + 65)
        else:
            ciphertxt += chr((((ord(plaintxt[i]) - 97) + key) % 26) + 97)
    print(f"ciphertext: {ciphertxt}")


def getShiftKey(key):
    shiftKey = []
    for char in key:
        if ord(char) >= 97:
            shiftKey.append(ord(char) - 97)
        else:
            shiftKey.append(ord(char) - 65)
    return shiftKey




if __name__ == '__main__':
    sys.exit(main())