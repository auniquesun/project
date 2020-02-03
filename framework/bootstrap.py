#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2019 *** (for blind review)
Date: 2019/11/14
"""

import argparse


def find_new_pattern(window_size):
    print('>>> start finding new patterns')
    # input parameter: known_pattern_words KPW
    phrases = []
    with open('seed.txt') as fin_seed:
        lines = fin_seed.readlines()
        for line in lines:
            if len(line.strip()) > 0:
                phrases.append(line.strip().split(', ')[2])

    new_patterns = []
    # input parameter: the group of titles
    file_titles_new = input('input titles file name: ')
    with open('../data/title/' + file_titles_new) as fin_titles_new:
        titles = fin_titles_new.readlines()
        for title in titles:
            for phrase in phrases:
                if phrase in title:
                    contexts = title.split(phrase)
                    prev_phrase = contexts[0].split(' ')[::-1]  # prev_phrase: from end to start
                    next_phrase = contexts[1].split(' ')    # next_phrase: from start to end
                    for idx, ele in enumerate(prev_phrase):
                        if idx < window_size:
                            new_patterns.append(ele)
                        else:
                            break
                    for idx, ele in enumerate(next_phrase):
                        if idx < window_size:
                            new_patterns.append(ele)
                        else:
                            break
    print('<<< find new patterns done')
    return new_patterns


def append_new_pattern(window_size, threshold):
    patterns = find_new_pattern(window_size)
    patt2counts = {}

    if len(patterns) > 0:
        with open('new_pattern_words.txt', 'w') as f:
            for pattern in patterns:
                # f.write(pattern + '\n')
                if pattern.lower() in patt2counts.keys():
                    patt2counts[pattern.strip().lower()] += 1
                else:
                    patt2counts[pattern.strip().lower()] = 1
    else:
        print('\n', '==>', 'new pattern not found', '<==', '\n')

    # output: new pattern words, which are stored in a .txt file
    # note: open the file with 'append' mode
    with open('new_pattern_words.txt', 'w') as f:
        # f.write('\n')
        for key in patt2counts.keys():
            if key.isalpha() and patt2counts[key] >= threshold:
                f.write(key.lower() + ' ' + str(patt2counts[key]) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input parameters of Bootstrapping Iteration.')
    parser.add_argument('-s', '--size', default=3, type=int, help='window size centered on the pattern word.')
    parser.add_argument('-i', '--iters', default=9, type=int, help='iterations of bootsrapping iteration.')
    parser.add_argument('-r', '--threshold', default=100, type=int, help='occurrences threshold of pattern words.')
    args = parser.parse_args()

    s = args.size
    iters = args.iters
    r = args.threshold

    for i in range(iters):
        append_new_pattern(s, r)
