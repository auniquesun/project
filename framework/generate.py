#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2019 *** (for blind review)
Date: 2019/11/14
"""

def generate_standard_data():
    print('>> starting building standard data')
    file_patt = input('fin > enter pattern file name: ')
    # input parameter: the dataset of titles
    file_title = input('fin > enter title file name: ')
    # output: standard datasets with labels whose format is consistent with CoNLL 2003
    file_train = input('fout < enter train file name: ')
    with open('pattern/' + file_patt) as fin_pattern, open('title/' + file_title) as fin_title, open('data/' + file_train, 'w') as fout:
        lines_pattern = fin_pattern.readlines()
        lines_title = fin_title.readlines()

        for line_title, line_pattern in zip(lines_title, lines_pattern):
            words = [word for word in line_title.strip().split(' ') if len(word) > 0]
            blocks = line_pattern.strip().split(', ')
            pattern = blocks[1]
            if len(blocks) > 3:
                pm1 = blocks[2]
                pm2 = blocks[3]

            for word in words:
                flag = False
                punctuation = None
                if ',' == word[-1] or '.' == word[-1] or ':' == word[-1]:
                    punctuation = word[-1]
                    word = word[0: len(word)-1]
                    flag = True
                # generate negative examples
                if pattern == 'P: None':
                    if len(word) > 0:
                        fout.write(word + ' O' + '\n')
                elif pattern == 'P: for':
                    if word.lower() in pm1.split(' '):
                        fout.write(word + ' M' + '\n')
                    elif word.lower() in pm2.split(' '):
                        fout.write(word + ' P' + '\n')
                    else:
                        if len(word) > 0:
                            fout.write(word + ' O' + '\n')
                else:
                    if word.lower() in pm1.split(' '):
                        fout.write(word + ' P' + '\n')
                    elif word.lower() in pm2.split(' '):
                        fout.write(word + ' M' + '\n')
                    else:
                        if len(word) > 0:
                            fout.write(word + ' O' + '\n')

                if flag:
                    fout.write(punctuation + ' O' + '\n')
                    self.line_index += 1
            fout.write('\n')
            self.line_index += 2
    print('<< build data done')


if __name__ == '__main__':
    generate_standard_data()
