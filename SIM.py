
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

originalCode = readFileLineByLine("original.txt")
dictionary = createDictionary(originalCode)

codeEntryIndex = 0
while codeEntryIndex < len(originalCode):
  print(originalCode[codeEntryIndex])
  codeEntryIndex = codeEntryIndex + 1


