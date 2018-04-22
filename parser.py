"""
CKY algorithm from the "Natural Language Processing" course by Michael Collins
https://class.coursera.org/nlangp-001/class
"""
import sys
from sys import stdin, stderr
from time import time
from json import dumps

from collections import defaultdict
from pprint import pprint

from pcfg import PCFG
from tokenizer import PennTreebankTokenizer


def argmax(lst):
    return max(lst) if lst else (0.0, None)


def backtrace(bpChart, bp):
    # ADD YOUR CODE HERE
    # Extract the tree from the backpointers
    print(bpChart)

    if len(bp) == 4:
        return [label, bp[back]]

    elif len(bp[back]) == 3:
        c1, c2, s = bp[back]
        return [label, backtrace((begin, s, c1), bp), backtrace((s, end, c2), bp)]


def CKY(pcfg, norm_words):
    # ADD YOUR CODE HERE
    # IMPLEMENT CKY

    # NOTE: norm_words is a list of pairs (norm, word), where word is the word
    #       occurring in the input sentence and norm is either the same word, 
    #       if it is a known word according to the grammar, or the string _RARE_. 
    #       Thus, norm should be used for grammar lookup but word should be used 
    #       in the output tree.

    # with reference https://github.com/usami/pcfg/blob/master/pcfg_parser.py

    # Initialize your charts (for scores and backpointers)
    n = len(norm_words)
    pi = defaultdict(float)
    bp = defaultdict(tuple)

    # Code for adding the words to the chart
    for i, (norm, word) in enumerate(norm_words):
        for c in pcfg.N:
            pi[i, i + 1, c] = pcfg.q1[(c, norm)]
            bp[i, i + 1, c] = (c, word, i, i+1)

    # Code for the dynamic programming part, where larger and larger subtrees are built
    for span in range(2, n + 1):
        for begin in range(n + 1 - span):
            end = begin + span
            for c in pcfg.N:
                best = 0
                bp_point = ()
                for c1, c2 in pcfg.binary_rules[c]:
                    for split in range(begin + 1, end):
                        if pi[begin, split, c1] and pi[split, end, c2]:
                            prob = pi[begin, split, c1] * pi[split, end, c2] * pcfg.q2[(c, c1, c2)]
                            if prob > best:
                                best = prob
                                bp_point = (c, c1, c2, begin, split, end)
                if best:
                    pi[begin, end, c] = best
                    bp[begin, end, c] = bp_point

    # Below is one option for retrieving the best trees, assuming we only want trees with the "S" category
    if pi[0, n, 'S']:
        return backtrace(bp[(0, n, 'S')], bp)
    # This is a simplification, since not all sentences are of the category "S"
    # The exact arguments also depends on how you implement your back-pointer chart.
    # Below it is also assumed that it is called "bp"
    # return backtrace(bp[0, n, "S"], bp)
    # else:
    #     best = 0
    #     bp_point = None
    #     for c in pcfg.N:
    #         if pi[0, n, c] > best:
    #             best = pi[0, n, c]
    #             bp_point = 0, n, c
    #     return backtrace(bp_point, bp, norm_words)


class Parser:
    def __init__(self, pcfg):
        self.pcfg = pcfg
        self.tokenizer = PennTreebankTokenizer()

    def parse(self, sentence):
        words = self.tokenizer.tokenize(sentence)
        norm_words = []
        for word in words:  # rare words normalization + keep word
            norm_words.append((self.pcfg.norm_word(word), word))
        tree = CKY(self.pcfg, norm_words)
        tree[0] = tree[0].split("|")[0]
        return tree


def display_tree(tree):
    pprint(tree)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python3 parser.py GRAMMAR")
        exit()

    start = time()
    grammar_file = sys.argv[1]
    print("Loading grammar from " + grammar_file + " ...", file=stderr)
    pcfg = PCFG()
    pcfg.load_model(grammar_file)
    parser = Parser(pcfg)

    print("Parsing sentences ...", file=stderr)
    for sentence in stdin:
        tree = parser.parse(sentence)
        print(dumps(tree))
    print("Time: (%.2f)s\n" % (time() - start), file=stderr)
