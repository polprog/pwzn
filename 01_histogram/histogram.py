#!/usr/bin/env python3 
# pwzn 2023 - projekt 01 - histogram
# Krzysztof Lasocki 13.10.23

import numpy as np
import argparse
import re
version = 1.0
args = None

def make_histogram(wordcount: dict):
    # sort dict by value, descending, return first N keys
    topkeys = sorted(wordcount, key=lambda x: wordcount[x],
                     reverse=True)[:args.num_words]
    print("##########")
    print(topkeys)
    if not topkeys:
        return
    # Normalize the histogram to 10
    maxhist = wordcount[max(topkeys, key=lambda x: wordcount[x])]
    print(f"maxhist={maxhist}")
    for key in topkeys:
        print(key, "\t","#" * int(30*wordcount[key]/maxhist))
    

def cleanup_words(words, ignores, specialchars="!;()-,—", filt=None, notfilt=None):
    """Clean up a line of words, lowercase, remove empty,
    remove specialchars (also utf-8 ones)
    @param filt: filter only words containing the given string"""
    reg = None
    nreg = None
    if filt:
        reg = re.compile(f'.*{filt}.*')
    if notfilt:
        nreg = re.compile(f'.*{notfilt}.*')
    newwords = []
    for word in words:
        if word in ignores:
            continue
        word = re.sub(rf'[{specialchars}]', "", word)
        if filt:
            if not reg.match(word):
                continue
        if notfilt:
            if nreg.match(word):
                continue
        if not word:
            continue
        newwords.append(word.lower())
    return newwords
        
def count_words(f, ignores=[], filt=None, notfilt=None):
    """Count words in the file, return dict of words and their counts
    words are converted to lower case first. This method does some 
    cleaning up (remove special chars, etc.)"""
    wordcount = {}
    for line in f:
        line = line.replace("\n", "") # chomp
        # XXX clean up special chars !?;() etc.
        if not line:
            continue
        words = line.split(" ")
        # Clean up words prior to counting
        for word in cleanup_words(words, ignores, filt=filt, notfilt=notfilt):
            if word not in wordcount:
                wordcount[word] = 0
            wordcount[word] = wordcount[word] + 1
    return wordcount


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='histogram',
        description='Draw a histogram of common words in input file',
        epilog=f'pwzn23, version {version} ')
    parser.add_argument('filename')
    parser.add_argument('-n', '--num-words',
                        help="Number of top words to print historgram for",
                        default=10, type=int)
    parser.add_argument('-l', '--min-length',
                        help="Minumum length of word (letters)", default=0)
    
    parser.add_argument('-i', '--ignore-words',
                        help="List of ignored words, comma separated")
    parser.add_argument('-I', '--ignore-str',
                        help="Ignore words containing given string")
    
    parser.add_argument('-m', '--match-str',
                        help="Count only words containing given string")
    parser.add_argument('-c', '--color', help="Assume VT525 or newer terminal",
                        action="store_true")
    parser.add_argument('-d', '--directory', help="Process all files in a given dir")
    parser.add_argument('-p', '--progress', help="")

    args = parser.parse_args()
    print(args)

    ignores = [word.lower() for word in args.ignore_words.split(",")]
    
    # FIXME: -d option

    if args.directory:
        # We have to iterate for all files in directory given by filename
        pass
    else:
        # Just this one file
        make_histogram(
            count_words(open(args.filename, "r"), ignores,
                        filt=args.match_str, notfilt=args.ignore_str)
        )
