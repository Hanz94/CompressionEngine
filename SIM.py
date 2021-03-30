# “I have neither given nor received any unauthorized aid on this assignment”.
# UFID -: 1163-9514
# Hansika Weerasena
import collections
import operator

dictionary = []


def readFileLineByLine(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    itemList = []
    for line in Lines:
        itemList.append(line.strip())
    file1.close()
    return itemList


def createDictionary(elements):
    counter = collections.Counter(elements)
    dictionary = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))
    return list(dictionary.keys())[:16]


def RLE(entry, index, originalCode):
    count = 0
    while entry == originalCode[index] and count < 9:
        count = count + 1
        index = index + 1
    return count

def exactMatch(codeEnty):
    try:
        return dictionary.index(codeEnty)
    except ValueError:
        return -1

def getXORedString(entry, dicEntry):
    y = int(entry, 2) ^ int(dicEntry, 2)
    return '{0:b}'.format(y)

def getXORedString(entry, dicEntry):
    y = int(entry, 2) ^ int(dicEntry, 2)
    return '{0:b}'.format(y)

originalCode = readFileLineByLine("original.txt")
dictionary = createDictionary(originalCode)

codeEntryIndex = 0
previousCodeEntry = ''
compressedCode = ''

while codeEntryIndex < len(originalCode):
    increment = 1
    if previousCodeEntry == originalCode[codeEntryIndex]:
        rle_count = RLE(previousCodeEntry, codeEntryIndex, originalCode)
        compressedEntry = '001' + bin(rle_count - 1)[2:].zfill(3)
        increment = rle_count
    else:
        exactMatchIndex = exactMatch(originalCode[codeEntryIndex])
        if exactMatchIndex > 0:
            compressedEntry = '111' + bin(exactMatchIndex)[2:].zfill(4)
        else:
            isMatched = False
            for dicEntry in dictionary:
                xorString = getXORedString(originalCode[codeEntryIndex])
                length = len(xorString)
                xorChunk =




    compressedCode = compressedCode + compressedEntry
    previousCodeEntry = originalCode[codeEntryIndex]
    codeEntryIndex = codeEntryIndex + increment
