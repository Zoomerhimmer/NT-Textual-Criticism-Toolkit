import re
import os
import argparse
from collections import Counter
from normalize import normalize, normalizer

punctuation = ['·', ',', ';', '.']
superscript = str.maketrans("0123456789,", "⁰¹²³⁴⁵⁶⁷⁸⁹ʼ")

# To avoid extra bracket insertion
def remove_dup(arr):
    new_arr = []
    [new_arr.append(x) for x in arr if x not in new_arr]
    return new_arr

# Lists are not hashable
def to_tuple(arr):
    new_arr = []
    for i in arr:
        new_arr.append(tuple(i))
    return new_arr

# Removes punctuation from all elements
def remove_punc(arr):
    new_arr = []
    for i in range(len(arr)):
        new_arr.append(arr[i])
        for j in range(len(arr[i])):
            new_arr[i][j] = normalizer(punctuation, '', arr[i][j])
    return new_arr

def main():
    parser = argparse.ArgumentParser(description='This program finds possible homeoteleuton locations. It takes in one file.')
    parser.add_argument('file', help='Name/path of the file to process.')
    parser.add_argument('-i', '--iota_subscript', action='store_true', help='Distinguish letters with an iota subscript.')
    parser.add_argument('-l', '--location_notation', action='store_true', help='Bracket entire locations rather than pairs.')
    parser.add_argument('-b', '--beginning_length', type=int, help='Minimum number of beginning letters to match.')
    args = parser.parse_args()

    # Ignore iota subscripts by default
    if args.iota_subscript:
        iota_subscript = True
    else:
        iota_subscript = False
    # Don't show locations by default
    if args.location_notation:
        show_loc = True
    else:
        show_loc = False
    # Beginning length is two by default
    if args.beginning_length is not None:
        if args.beginning_length > 0:
            beg_len = args.beginning_length
        else:
            sys.exit("Beginning_length needs to be larger than zero.")
    else:
        beg_len = 2

    # Open files
    input = open(args.file)
    data = input.read()
    filename = os.path.splitext(args.file)[0] + '_results.txt'
    output = open(filename, 'w')

    data = normalize(data, not iota_subscript) # Normalize uses ignore_subscript boolean
    pairs_pattern = re.compile(fr'(\b(?P<begin>\w{{{beg_len},}})\w*\b\S?\s+\b(?P=begin)\w*\b)')
    loc_pattern = re.compile(fr'''
            (\b(?P<begin>\w{{{beg_len},}}?)
            \w*\b
            (\S?                    # To allow punctuation at the end of the first word
            \s+                     # The whitespace separating the two words
            \b(?P=begin)\w*\b)+)
            ''', re.X)
    loc_total = len(loc_pattern.findall(data)) # finditer returns unique matches
    locations = []
    for match in loc_pattern.finditer(data):
        loc_string = match.group()
        location = match.group().split()
        location.append(loc_string)
        locations.append(location)
    # Add bracketing for locations
    prettified = data
    if show_loc:
        for loc in locations:
            prettified = re.sub(fr'(\b{loc[-1]}\b)', r'(\1)', prettified)
        # Inefficient, but it works for odd ranges of words (can't find a regex that removes recursively); still allows (( bug
        nested_braces = re.compile(r'(\([^)(]*)\(([^)(]*)\)([^)(]*\))')
        while nested_braces.search(prettified):
            prettified = nested_braces.sub(r'\1\2\3', prettified) # Removes nested braces

    # Construct pairs from locations
    locations = remove_punc(locations)
    pairs = []
    for loc in locations:
        for i in range(1, len(loc)-1): # Do not pickup the final element which is the location string
            pairs.append([loc[i-1], loc[i]])

    # Add pairing brackets
    pruned_pairs = remove_dup(pairs)
    print(pruned_pairs)
    pairs_total = 0
    for pair in pruned_pairs:
        pair_pattern = re.compile(fr'(\b{pair[0]}\b\S?[]]?\s+[[⁰¹²³⁴⁵⁶⁷⁸⁹ʼ]*\b{pair[1]}\b\S?)')
        if show_loc:
            pairs_total += len(pair_pattern.findall(data)) # Get count from data to avoid (( bug
        else:
            beg_len_num = str(len(pairs_pattern.search(f'{pair[0]} {pair[1]}').group('begin'))).translate(superscript)
            occurences = len(pair_pattern.findall(prettified))
            pairs_total += occurences # Given that pairs are unique
            occurences = ',' + str(occurences)
            occurences = occurences.translate(superscript)
            prettified = pair_pattern.sub(fr'{beg_len_num}{occurences}[\1]', prettified)
    output.write(prettified)
    output.write(f'\n\nTotal possible homoioarcton locations: {loc_total}')
    output.write(f'\nTotal pairs: {pairs_total}')

    # Close files
    input.close()
    output.close()

if __name__ == '__main__':
    main()
