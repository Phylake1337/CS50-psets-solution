from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    list1 = a.split('\n')
    list2 = b.split('\n')

    output = []

    for line in list1:
        if line in output:
            continue
        elif line in list2:
            output.append(line)
    return output


def sentences(a, b):
    """Return sentences in both a and b"""

    list1 = sent_tokenize(a, language='english')
    list2 = sent_tokenize(b, language='english')

    output = []

    for line in list1:
        if line in output:
            continue
        elif line in list2:
            output.append(line)
    return output


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    output = []

    for i in range(len(a)-n+1):
        if a[i : i + n] in output:
            continue
        elif a[i : i + n] in b:
            output.append(a[i : i + n])
    return output
