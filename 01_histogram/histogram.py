#!/usr/bin/env python3 
# pwzn 2023 - projekt 01 - histogram
# Krzysztof Lasocki 13.10.23

import numpy as np
import argparse
import re
from tqdm import tqdm
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from ascii_graph.colordata import hcolor

version = 1.0
args = None

def make_histogram(wordcount: dict):
    # sort dict by value, descending, return first N keys
    topkeys = sorted(wordcount, key=lambda x: wordcount[x],
                     reverse=True)[:args.num_words]
    if not topkeys:
        return
    # Normalize the histogram to 30
    maxhist = wordcount[max(topkeys, key=lambda x: wordcount[x])]
    if not args.color:
        for key in topkeys:
            print(key, "\t","#" * int(30*wordcount[key]/maxhist), wordcount[key])
    else:
        grdata = [(key, wordcount[key]) for key in topkeys]
        graph = Pyasciigraph()
        pattern = [Gre, Yel, Red, Cya, Pur]
        data = vcolor(grdata, pattern)
        for line in  graph.graph('Word histogram', data):
            print(line)
            

def cleanup_words(words, ignores, specialchars="!;:()-,—?.", filt=None, notfilt=None, min_len=None):
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
        if ignores and word in ignores:
            continue
        word = re.sub(rf'[{specialchars}]', "", word)
        if min_len:
            if len(word) < min_len:
                continue
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
        
def count_words(f, ignores=[], filt=None, notfilt=None, min_len=None):
    """Count words in the file, return dict of words and their counts
    words are converted to lower case first. This method does some 
    cleaning up (remove special chars, etc.)"""
    wordcount = {}
    # Usually too fast to see the program run
    for line in tqdm(f):
        line = line.replace("\n", "") # chomp
        if not line:
            continue
        words = line.split(" ")
        # Clean up words prior to counting
        for word in cleanup_words(words, ignores, filt=filt, notfilt=notfilt, min_len=min_len):
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
                        help="Minumum length of word (letters)", type=int)
    
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

    ignores = None
    if args.ignore_words:
        ignores = [word.lower() for word in args.ignore_words.split(",")]

    # FIXME: -d option
    if args.directory:
        # We have to iterate for all files in directory given by filename
        pass
    else:
        # Just this one file
        make_histogram(
            count_words(open(args.filename, "r"), ignores,
                        filt=args.match_str, notfilt=args.ignore_str, min_len=args.min_length)
        )
