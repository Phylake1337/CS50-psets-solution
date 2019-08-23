from cs50 import get_int

def main():
    #Take a number
    credNum = str(get_int("Number: "))
    #Check its type
    credType = typeCheck(credNum)
    if credType == "INVALID":
        print("INVALID")
    else:
        #Check Sum
        checkSum(credNum, credType)

def typeCheck(credNum):
    credType = ""
    if credNum[0] == "4":
        credType = "VISA"

    elif credNum[:2] in ["34", "37"]:
        credType = "AMEX"

    elif credNum[:2] in ["51", "52", "53", "54", "55"]:
        credType = "MASTERCARD"

    else:
        credType = "INVALID"
    return credType

def checkSum(credNum, credType):
    credNum = list(credNum[::-1])
    outNum = []

    for i in range(len(credNum)):
        if i % 2 == 0:
            outNum.append(int(credNum[i]))

        else:
            nChar = credNum[i]
            nChar = str(int(nChar) * 2)

            if int(nChar) > 9:
                listChar = list(nChar)
                for i in listChar[::-1]:
                    outNum.append(int(i))
            else:
                outNum.append(int(nChar))

    Sum = sum(outNum)
    if Sum % 10 == 0:
        print(credType)
    else:
        print("INVALID")

if __name__ == '__main__':
    main()