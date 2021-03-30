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
    while entry == originalCode[index] and count < 8:
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


def getXORedChunk(str):
    x = str.rfind('1')
    y = str.find('1')
    return str[y:x+1]


def chunkstring(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))


def writeToFile(compressedCode):
    open('somefile.txt', 'w').close()
    compressedEntries = chunkstring(compressedCode, 32)
    with open('somefile.txt', 'a') as the_file:
        for i in range(len(compressedEntries)):
            the_file.write(compressedEntries[i].ljust(32, '0') + "\n")
        the_file.write('xxxx\n')
        for entries in dictionary:
            the_file.write(entries + "\n")


originalCode = readFileLineByLine("original.txt")
dictionary = createDictionary(originalCode)

# originalCode = readFileLineByLine("sample.txt")

codeEntryIndex = 0
previousCodeEntry = ''
# compressedCode = []
compressedCode = ''

while codeEntryIndex < len(originalCode):
    increment = 1
    reset_flag = False
    if previousCodeEntry == originalCode[codeEntryIndex]:
        rle_count = RLE(previousCodeEntry, codeEntryIndex, originalCode)
        compressedEntry = '001' + bin(rle_count - 1)[2:].zfill(3)
        increment = rle_count
        if rle_count == 8:
            reset_flag = True
    else:
        exactMatchIndex = exactMatch(originalCode[codeEntryIndex])
        if exactMatchIndex >= 0:
            compressedEntry = '111' + bin(exactMatchIndex)[2:].zfill(4)
        else:
            isMatched = False
            for i in range(len(dictionary)):
                xorString = getXORedString(originalCode[codeEntryIndex], dictionary[i])
                length = len(xorString)
                xorChunk = getXORedChunk(xorString)
                if int(xorChunk, 2) == 1:
                    compressedEntry = '011' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                    isMatched = True
                    break
                elif int(xorChunk, 2) == 3:
                    compressedEntry = '100' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                    isMatched = True
                    break
                elif int(xorChunk, 2) == 15:
                    compressedEntry = '101' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                    isMatched = True
                    break
                else:
                    continue
            if not isMatched:
                for i in range(len(dictionary)):
                    xorString = getXORedString(originalCode[codeEntryIndex], dictionary[i])
                    length = len(xorString)
                    xorChunk = getXORedChunk(xorString)
                    if len(xorChunk) < 5:
                        xorChunk = xorChunk.ljust(4, '0')
                        compressedEntry = '010' + bin(32 - length)[2:].zfill(5) + xorChunk + bin(i)[2:].zfill(4)
                        isMatched = True
                        break
                if not isMatched:
                    for i in range(len(dictionary)):
                        xorString = getXORedString(originalCode[codeEntryIndex], dictionary[i])
                        length = len(xorString)
                        xorChunk = getXORedChunk(xorString)
                        if xorChunk.count('1') == 2:
                            firstIndex = 32 - length
                            secondIndex = firstIndex + xorChunk.rfind('1')
                            compressedEntry = '110' + bin(firstIndex)[2:].zfill(5) + bin(secondIndex)[2:].zfill(5) + bin(i)[2:].zfill(4)
                            isMatched = True
                            break
                    if not isMatched:
                        compressedEntry = '000' + originalCode[codeEntryIndex]

    # compressedCode.append(compressedEntry)
    compressedCode = compressedCode + compressedEntry
    previousCodeEntry = originalCode[codeEntryIndex]
    if reset_flag:
        previousCodeEntry = ''
    codeEntryIndex = codeEntryIndex + increment

writeToFile(compressedCode)
