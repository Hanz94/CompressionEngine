# “I have neither given nor received any unauthorized aid on this assignment”.
# UFID -: 1163-9514
# Hansika Weerasena

import collections
import operator
import sys


def read_file_line_by_line(filename):
    file1 = open(filename, 'r')
    lines = file1.readlines()
    item_list = []
    for line in lines:
        item_list.append(line.strip())
    file1.close()
    return item_list


def create_dictionary(elements):
    counter = collections.Counter(elements)
    dictionary = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))
    return list(dictionary.keys())[:16]


def rle(entry, index, original_code):
    count = 0
    while entry == original_code[index] and count < 8:
        count = count + 1
        index = index + 1
    return count


def exact_match(code_entry, dictionary):
    try:
        return dictionary.index(code_entry)
    except ValueError:
        return -1


def get_xored_string(entry, dic_entry):
    y = int(entry, 2) ^ int(dic_entry, 2)
    return '{0:b}'.format(y)


def get_xored_chunk(str):
    x = str.rfind('1')
    y = str.find('1')
    return str[y:x+1]


def chunk_string(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))


def write_compression_to_file(compressed_code, dictionary):
    open('cout.txt', 'w').close()
    compressed_entries = chunk_string(compressed_code, 32)
    with open('cout.txt', 'a') as the_file:
        for i in range(len(compressed_entries)):
            the_file.write(compressed_entries[i].ljust(32, '0') + "\n")
        the_file.write('xxxx\n')
        for entries in dictionary:
            the_file.write(entries + "\n")


def write_decompression_to_file(decompressed_code):
    open('dout.txt', 'w').close()
    with open('dout.txt', 'a') as the_file:
        for entries in decompressed_code:
            the_file.write(entries + "\n")


def compress():
    original_code = read_file_line_by_line("original.txt")
    dictionary = create_dictionary(original_code)

    code_entry_index = 0
    previous_code_entry = ''
    compressed_code = ''

    while code_entry_index < len(original_code):
        increment = 1
        reset_flag = False
        compressed_entry = ''
        if previous_code_entry == original_code[code_entry_index]:
            rle_count = rle(previous_code_entry, code_entry_index, original_code)
            compressed_entry = '001' + bin(rle_count - 1)[2:].zfill(3)
            increment = rle_count
            if rle_count == 8:
                reset_flag = True
        else:
            exact_match_index = exact_match(original_code[code_entry_index], dictionary)
            if exact_match_index >= 0:
                compressed_entry = '111' + bin(exact_match_index)[2:].zfill(4)
            else:
                is_matched = False
                for i in range(len(dictionary)):
                    xor_string = get_xored_string(original_code[code_entry_index], dictionary[i])
                    length = len(xor_string)
                    xor_chunk = get_xored_chunk(xor_string)
                    if int(xor_chunk, 2) == 1:
                        compressed_entry = '011' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                        is_matched = True
                        break
                    elif int(xor_chunk, 2) == 3:
                        compressed_entry = '100' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                        is_matched = True
                        break
                    elif int(xor_chunk, 2) == 15:
                        compressed_entry = '101' + bin(32 - length)[2:].zfill(5) + bin(i)[2:].zfill(4)
                        is_matched = True
                        break
                    else:
                        continue
                if not is_matched:
                    for i in range(len(dictionary)):
                        xor_string = get_xored_string(original_code[code_entry_index], dictionary[i])
                        length = len(xor_string)
                        xor_chunk = get_xored_chunk(xor_string)
                        if len(xor_chunk) < 5:
                            xor_chunk = xor_chunk.ljust(4, '0')
                            compressed_entry = '010' + bin(32 - length)[2:].zfill(5) + xor_chunk + bin(i)[2:].zfill(4)
                            is_matched = True
                            break
                    if not is_matched:
                        for i in range(len(dictionary)):
                            xor_string = get_xored_string(original_code[code_entry_index], dictionary[i])
                            length = len(xor_string)
                            xor_chunk = get_xored_chunk(xor_string)
                            if xor_chunk.count('1') == 2:
                                first_index = 32 - length
                                second_index = first_index + xor_chunk.rfind('1')
                                compressed_entry = '110' + bin(first_index)[2:].zfill(5) + bin(second_index)[2:].zfill(5) + bin(i)[2:].zfill(4)
                                is_matched = True
                                break
                        if not is_matched:
                            compressed_entry = '000' + original_code[code_entry_index]

        compressed_code = compressed_code + compressed_entry
        previous_code_entry = original_code[code_entry_index]
        if reset_flag:
            previous_code_entry = ''
        code_entry_index = code_entry_index + increment

    write_compression_to_file(compressed_code, dictionary)


def pop_substring(str, len):
    return str[:len], str[len:]


def get_dict_index(compressed_entries):
    dict_index, compressed_entries = pop_substring(compressed_entries, 4)
    dict_index = int(dict_index, 2)
    return dict_index, compressed_entries


def get_starting_index(compressed_entries):
    dict_index, compressed_entries = pop_substring(compressed_entries, 5)
    dict_index = int(dict_index, 2)
    return dict_index, compressed_entries


def create_bitmask(bitmask_str, adjusting_bits):
    bitmask_str = bitmask_str.ljust(adjusting_bits, '0')
    return int(bitmask_str, 2)


def apply_bitmask(bitmask, dictionary_entry):
    return [bin(bitmask ^ int(dictionary_entry, 2))[2:].zfill(32)]


def decompress_entry_for_consecutive_mask(bitmask_str, starting_index, compressed_entries, dictionary):
    bitmask = create_bitmask(bitmask_str, 32 - starting_index)
    dict_index, compressed_entries = get_dict_index(compressed_entries)
    return apply_bitmask(bitmask, dictionary[dict_index]), compressed_entries


def process_compressed_entries(compressed_entries, dictionary, previous_entry):
    decompressed = []
    compressed_type, compressed_entries = pop_substring(compressed_entries, 3)
    if compressed_type == '000':
        original, compressed_entries = pop_substring(compressed_entries, 32)
        if len(original) == 32:
            decompressed = [original]
    elif compressed_type == '001':
        run_length, compressed_entries = pop_substring(compressed_entries, 3)
        run_length = int(run_length, 2)
        decompressed = [previous_entry[0] for i in range(run_length+1)]
    elif compressed_type == '111':
        dict_index, compressed_entries = get_dict_index(compressed_entries)
        decompressed = [dictionary[dict_index]]
    elif compressed_type == '010':
        starting_index, compressed_entries = get_starting_index(compressed_entries)
        bitmask_str, compressed_entries = pop_substring(compressed_entries, 4)
        decompressed, compressed_entries = decompress_entry_for_consecutive_mask(bitmask_str, starting_index, compressed_entries, dictionary)
    elif compressed_type == '011':
        starting_index, compressed_entries = get_starting_index(compressed_entries)
        decompressed, compressed_entries = decompress_entry_for_consecutive_mask('1', starting_index, compressed_entries, dictionary)
    elif compressed_type == '100':
        starting_index, compressed_entries = get_starting_index(compressed_entries)
        decompressed, compressed_entries = decompress_entry_for_consecutive_mask('11', starting_index, compressed_entries, dictionary)
    elif compressed_type == '101':
        starting_index, compressed_entries = pop_substring(compressed_entries, 5)
        starting_index = int(starting_index, 2)
        decompressed, compressed_entries = decompress_entry_for_consecutive_mask('1111', starting_index, compressed_entries, dictionary)
    elif compressed_type == '110':
        starting_index_1, compressed_entries = get_starting_index(compressed_entries)
        starting_index_2, compressed_entries = get_starting_index(compressed_entries)
        bitmask_str = '1'
        bitmask_str = bitmask_str.ljust(starting_index_2 - starting_index_1, '0')
        bitmask_str = bitmask_str + '1'
        bitmask_str = bitmask_str.ljust(32 - starting_index_1, '0')
        bitmask = int(bitmask_str, 2)
        dict_index, compressed_entries = get_dict_index(compressed_entries)
        decompressed = apply_bitmask(bitmask, dictionary[dict_index])
    else:
        compressed_entries = ''
    return decompressed, compressed_entries


def decompress():
    decompressed = []
    compressed = read_file_line_by_line('compressed.txt')
    split_index = compressed.index('xxxx')
    compressed_entries_list = compressed[0:split_index]
    dictionary = compressed[split_index+1:]
    compressed_entries = ''.join(compressed_entries_list)

    decompressed_entry = ''
    while len(compressed_entries) > 0:
        decompressed_entry, compressed_entries = process_compressed_entries(compressed_entries, dictionary, decompressed_entry)
        decompressed = decompressed + decompressed_entry
    write_decompression_to_file(decompressed)


if sys.argv[1] == '1':
    compress()
else:
    decompress()
