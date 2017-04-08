#!/usr/bin/env python

"""
Usage:
    countdown <letters> [--word_list=<wordlist>] [--min=<word_length>]
"""

import itertools
import collections
import pprint
import sys
import re
import os.path
import pickle
from docopt import docopt


class countdown_word_solver(object):
    def __init__(self, dictionary_name, threshold=5):
        self.threshold = int(threshold) if threshold else 5

        if dictionary_name:
            self.wordlist = sorted(list(set(
                                            [word.strip().lower()
                                            for word
                                            in open(dictionary_name, 'r')]
                                            )))

            self.make_anagram_dict(self.wordlist)
        elif os.path.isfile('anagram_dict'):
            self.anagram_dict = self.load_anagram_dict()
        else:
            raise ValueError('No wordlist file is specified and no anagram_dict exists')

    def load_anagram_dict(self):
        with open('anagram_dict', 'rb') as f:
            self.anagram_dict = pickle.load(f)
            return self.anagram_dict

    def save_anagram_dict(self, anagram_dict):
        with open('anagram_dict', 'wb') as f:
            pickle.dump(anagram_dict, f, pickle.HIGHEST_PROTOCOL)

    def make_anagram_dict(self, word_dict):
        self.anagram_dict = collections.defaultdict(list)

        for word in word_dict:
            self.anagram_dict[self.signature(word)].append(word)

        self.save_anagram_dict(self.anagram_dict)
        return self.anagram_dict

    def signature(self, word):
        return ''.join(sorted(word)).lower()

    def fast_anagram(self, word):
        return self.anagram_dict[self.signature(word)]

    def find_words(self, letters):
        words = collections.defaultdict(list)

        for i in range(self.threshold, len(letters) + 1):
            combos = itertools.combinations(letters, i)
            for combo in combos:
                words[len(combo)].extend(self.fast_anagram(''.join(combo)))

        for key, word_list in words.items():
            words[key] = set(word_list)

        return words

if '__main__' == __name__:
    args = docopt(__doc__, argv=sys.argv[1:])
    pp = pprint.PrettyPrinter(indent=2)

    wordlist = args['--word_list']
    letters = re.findall("[a-zA-Z]", args['<letters>'])

    solver = countdown_word_solver(wordlist, args['--min'])
    words = solver.find_words(letters)

    pp.pprint(words)

