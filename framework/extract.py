#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2020 *** (for blind review)
Date: 2020/02/11
"""


def pattern_phrase_extraction():
    print('>> starting building standard pattern')

    # input parameter: the set of known pattern words, KPW
    # note: after bootstrapping iteration, the KPW has been merged with NPW so the KPW contains latest modification.
    patterns = []
    with open('known_pattern_words.txt') as fin:
        lines = fin.readlines()
        for line in lines:
            if len(line.strip()) > 0 and '#' not in line:   # skip blank line and commented line
                patterns.append(line.strip())

    pos_examples, neg_examples = [], []
    # input parameter: the dataset of titles
    file_title = input('fin > enter title file name: ')
    # output: patterns in titles containing label id information
    file_patt = input('fout < enter pattern file name: ')
    file_title_real = input('fout < enter real title file name: ')
    with open('title/' + file_title) as fin, open('pattern/' + file_patt, 'w') as fout, \
            open('title/' + file_title_real, 'w') as fout_real:
        lines = fin.readlines()
        for index, line in enumerate(lines):
            if len(pos_examples) >= 500000 and len(neg_examples) >= 500000:
                break
            if len(line.strip()) != 0:
                tokens = line.split(' ')
                tokens = [token for token in tokens if len(token) > 0]
                # for this case: 'Shift-Net: Image Inpainting via Deep Feature Rearrangement', remove its first word
                # because these cases have great influcen on chunking
                if len(tokens):
                    print(index+1, '-->', tokens[0], '-->')
                if len(tokens) > 0 and tokens[0][-1] == ':':
                    del tokens[0]
                # convert token to the form of lower case
                tokens_lower = [token.lower() for token in tokens]
                # count to record the title which didn't contain any pattern
                count = 0
                written_pattern = False
                written_none = False
                for pattern in patterns:
                    flag = False
                    # pattern is lower case
                    if pattern == 'based on':
                        if 'based' in tokens_lower and 'on' in tokens_lower:
                            if tokens_lower.index('on') - tokens_lower.index('based') == 1:
                                flag = True
                    if pattern in tokens_lower or flag:
                        # make sure that a single word containing specific patterns won't be split
                        if flag == False:
                            idx = tokens_lower.index(pattern)
                            former = tokens[:idx]
                            latter = tokens[idx+1:]
                        else:
                            idx = tokens_lower.index('based')
                            former = tokens[:idx]
                            latter = tokens[idx+2:]

                        former = self.extract_candidate_chunks(' '.join(former))
                        latter = self.extract_candidate_chunks(' '.join(latter))
                        if len(former) > 0 and len(latter) > 0:
                            if len(pos_examples) < 500000:
                                pos_examples.append(str(index+1) + ', P: ' + pattern + ', ' + former[0] + ', ' + latter[0] + '\n')
                                fout_real.write(line)
                                self.line_index += 1
                                # fout wrote a title containing pattern, set 'written_pattern' true for breaking loop
                                written_pattern = True
                        else:
                            """
                            句子中存在pattern word，但是len(former)，len(latter)中至少一个为0
                            例，Using GLRPPR (and other P2Rx Centers) to Identify
                            Hazardous Substance Reduction Resources
                            从这个例子想到另一个pattern，using ... to ...
                            """
                            written_none = True
                    if pattern not in tokens_lower and flag == False: # pattern word didn't appear in the sentence
                        count += 1
                    if written_pattern:
                        break
                """
                case one: the sentence didn't contain any pattern word
                case two: there is a pattern word in the sentence but, len(former) or len(latter) equals 0 after chunking
                """
                # case one: the sentence didn't contain any pattern word
                # case two: there is a pattern word in the sentence but, len(former) or len(latter) equals 0 after chunking
                if count == len(patterns) or (not written_pattern and written_none):
                    if len(neg_examples) < 500000:
                        neg_examples.append(str(index+1) + ', P: None' + '\n')
                        fout_real.write(line)
        for pos, neg in zip(pos_examples, neg_examples):
            fout.write(pos)
            fout.write(neg)
        print('pos_examples:', len(pos_examples))
        print('neg_examples:', len(neg_examples))
    print('<< build pattern done')


if __name__ == '__main__':
    pattern_phrase_extraction()

