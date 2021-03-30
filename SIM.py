# “I have neither given nor received any unauthorized aid on this assignment”.
# UFID -: 1163-9514
# Hansika Weerasena

import collections
import operator
import sys

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


def exactMatch(codeEnty, dictionary):
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


def writeToFile(compressedCode, dictionary):
    open('somefile.txt', 'w').close()
    compressedEntries = chunkstring(compressedCode, 32)
    with open('somefile.txt', 'a') as the_file:
        for i in range(len(compressedEntries)):
            the_file.write(compressedEntries[i].ljust(32, '0') + "\n")
        the_file.write('xxxx\n')
        for entries in dictionary:
            the_file.write(entries + "\n")

def writeToFile2(decompressedCode):
    open('somefile2.txt', 'w').close()
    with open('somefile2.txt', 'a') as the_file:
        for entries in decompressedCode:
            the_file.write(entries + "\n")


def compress():
    dictionary = []

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
            exactMatchIndex = exactMatch(originalCode[codeEntryIndex], dictionary)
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

    writeToFile(compressedCode, dictionary)


def popSubstring(str, len):
    return str[:len], str[len:]


def processCompressedEntries(compressed_entries, dictionary, previous_entry):
    decompressed = []
    compressed_type, compressed_entries = popSubstring(compressed_entries, 3)
    if compressed_type == '000':
        original, compressed_entries = popSubstring(compressed_entries, 32)
        if len(original) == 32:
            decompressed = [original]
    elif compressed_type == '001':
        run_length, compressed_entries = popSubstring(compressed_entries, 3)
        run_length = int(run_length, 2)
        decompressed = [previous_entry[0] for i in range(run_length+1)]
    elif compressed_type == '111':
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        decompressed = [dictionary[dict_index]]
    elif compressed_type == '010':
        starting_index, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index = int(starting_index, 2)
        bitmask_str, compressed_entries = popSubstring(compressed_entries, 4)
        bitmask_str = bitmask_str.ljust(32 - starting_index, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        result = bitmask ^ int(dictionary[dict_index], 2)
        decompressed = [bin(result)[2:].zfill(32)]
    elif compressed_type == '011':
        starting_index, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index = int(starting_index, 2)
        bitmask_str = '1'
        bitmask_str = bitmask_str.ljust(32 - starting_index, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        result = bitmask ^ int(dictionary[dict_index], 2)
        decompressed = list(bin(result)[2:].zfill(32))
    elif compressed_type == '100':
        starting_index, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index = int(starting_index, 2)
        bitmask_str = '11'
        bitmask_str = bitmask_str.ljust(32 - starting_index + 1, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        result = bitmask ^ int(dictionary[dict_index], 2)
        decompressed = [bin(result)[2:].zfill(32)]
    elif compressed_type == '101':
        starting_index, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index = int(starting_index, 2)
        bitmask_str = '1111'
        bitmask_str = bitmask_str.ljust(32 - starting_index + 3, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        result = bitmask ^ int(dictionary[dict_index], 2)
        decompressed = [bin(result)[2:].zfill(32)]
    elif compressed_type == '110':
        starting_index_1, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index_1 = int(starting_index_1, 2)
        starting_index_2, compressed_entries = popSubstring(compressed_entries, 5)
        starting_index_2 = int(starting_index_2, 2)
        bitmask_str = '1'
        bitmask_str = bitmask_str.ljust(starting_index_2 - starting_index_1, '0')
        bitmask_str = bitmask_str + '1'
        bitmask_str = bitmask_str.ljust(32 - starting_index_1, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = popSubstring(compressed_entries, 4)
        dict_index = int(dict_index, 2)
        result = bitmask ^ int(dictionary[dict_index], 2)
        decompressed = [bin(result)[2:].zfill(32)]
    else:
        compressed_entries = ''
    return decompressed, compressed_entries


def decompress():
    decompressed = []
    compressed= readFileLineByLine('compressed.txt')
    splitIndex = compressed.index('xxxx')
    compressedEntriesList = compressed[0:splitIndex]
    dictionary = compressed[splitIndex+1:]
    compressedEntries = ''.join(compressedEntriesList)

    decompreseedEntry = ''
    while len(compressedEntries) > 0:
        decompreseedEntry, compressedEntries = processCompressedEntries(compressedEntries, dictionary, decompreseedEntry)
        decompressed = decompressed + decompreseedEntry
    writeToFile2(decompressed)

decompress()
print('Hans')