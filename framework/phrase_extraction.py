#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2019 *** (for blind review)
Date: 2019/11/14
"""

def pattern_phrase_extraction():
    print('>> starting building standard pattern')
    patterns = []
    with open('pattern_words.txt') as fin:
        lines = fin.readlines()
        for line in lines:
            if len(line.strip()) > 0 and '#' not in line:   # 去掉空行，注释行
                patterns.append(line.strip())

    pos_examples, neg_examples = [], []
    file_title = input('fin > enter title file name: ')
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
                # 删除 'Shift-Net: Image Inpainting via Deep Feature Rearrangement' 第一个词
                # 标题中这种情况很多，对chunk影响比较大
                if len(tokens):
                    print(index+1, '-->', tokens[0], '-->')
                if len(tokens) > 0 and tokens[0][-1] == ':':
                    del tokens[0]
                # token 可能是大写/小写，统一转换成小写
                tokens_lower = [token.lower() for token in tokens]
                # 用来标记不包含 pattern 的title
                count = 0
                written_pattern = False
                written_none = False
                for pattern in patterns:
                    flag = False
                    # pattern 都是小写
                    if pattern == 'based on':
                        if 'based' in tokens_lower and 'on' in tokens_lower:
                            if tokens_lower.index('on') - tokens_lower.index('based') == 1:
                                flag = True
                    if pattern in tokens_lower or flag:
                        #保证不会出现某个词包含pattern，然后把这个词切分的情况
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
                                written_pattern = True  # 如果写入一个 pattern 对应的title，把count记作-2，用来break这个循环                                
                        else:
                            """
                            句子中存在pattern word，但是len(former)，len(latter)中至少一个为0
                            例，Using GLRPPR (and other P2Rx Centers) to Identify 
                            Hazardous Substance Reduction Resources
                            从这个例子想到另一个pattern，using ... to ...
                            """                       
                            written_none = True
                    if pattern not in tokens_lower and flag == False: # pattern word不在句子里头
                        count += 1
                    if written_pattern:
                        break
                if count == len(patterns) or (not written_pattern and written_none):  # 没有一个pattern word在句子里头，或者句子里有pattern word，但是chunk之后的former/latter有一个为空
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