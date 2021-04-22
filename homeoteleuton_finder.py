import re
import os
import argparse
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

    # Open files
    input = open(args.file)
    data = input.read()
    filename = os.path.splitext(args.file)[0] + '_results.txt'
    output = open(filename, 'w')

    data = normalize(data, not iota_subscript) # Normalize uses ignore_subscript boolean
    pairs_pattern = re.compile(r'(\b\w*?(?P<ending>\w{2,})\b\S?\s+\w*(?P=ending)\b)')
    loc_pattern = re.compile(r'''
            (\b\w*?                 # Grab beginning of the first word with lazy match
            (?P<ending>\w{2,})\b    # Captures at least two letters at the end of a word
            (\S?                    # To allow punctuation at the end of the first word
            \s+                     # The whitespace separating the two words
            \w*(?P=ending)\b)+)     # Repeat words with ending at least once
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
        # Inefficient, but it works for odd ranges of words (can't find a regex that removes recursively); allows (( bug
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
    pairs_total = 0
    for pair in pruned_pairs:
        pair_pattern = re.compile(fr'(\b{pair[0]}\b\S?[]⁰¹²³⁴⁵⁶⁷⁸⁹ʼ]*\s+[[]?{pair[1]}\b\S?)')
        if show_loc:
            pairs_total += len(pair_pattern.findall(data)) # Get count from data to avoid (( bug
        else:
            end_len_num = str(len(pairs_pattern.search(f'{pair[0]} {pair[1]}').group('ending'))).translate(superscript)
            occurences = len(pair_pattern.findall(prettified))
            pairs_total += occurences # Given that pairs are unique
            occurences = ',' + str(occurences)
            occurences = occurences.translate(superscript)
            prettified = pair_pattern.sub(fr'[\1]{end_len_num}{occurences}', prettified)
    output.write(prettified)
    output.write(f'\n\nTotal possible homeoteleuton locations: {loc_total}')
    output.write(f'\nTotal pairs: {pairs_total}')

    # Close files
    input.close()
    output.close()

if __name__ == '__main__':
    main()
