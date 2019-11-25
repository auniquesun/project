#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright 2019 *** (for blind review)
# Time:2019/11/14
"""

"""
1. 用训练好的模型，在测试集上预测
2. 拿到预测结果，对每个预测PM之间的词计数
3. 取2中的介词？从大到小排序，且满足 # prep > threshold, 再取 top K？
4. 把选出来的词加入 pattern_words.txt
5. 再次生成标注数据，重新训练模型
6. 重复1~5，直到发现不了新的介词？

[ --> 上述方法验证之后不可行 <-- ]
训练好的模型，拿来预测新的title，如果title中不含预定义的pattern，
根本不会同时标出其中的P、M

[ --> 新的思路 <-- ]
1. 拿seed.txt中的 phrase 到文本匹配，大约有100个phrase
2. 又出现了新的问题，title 有60万行，这样匹配的话 600K * 100，非常耗时
3. 抽取新的title，取10万行即可
"""

def find_new_pattern():
    print('>>> start finding new patterns')
    phrases = []
    with open('seed.txt') as fin_seed:
        lines = fin_seed.readlines()
        for line in lines:
            if len(line.strip()) > 0:
                phrases.append(line.strip().split(', ')[2])

    new_patterns = []
    file_titles_new = input('input titles file name: ')
    with open('title/' + file_titles_new) as fin_titles_new:
        titles = fin_titles_new.readlines()
        for title in titles:
            for phrase in phrases:
                if phrase in title:
                    contexts = title.split(phrase)
                    prev_phrase = contexts[0].split(' ')[::-1]  # prev 从end到start取元素
                    next_phrase = contexts[1].split(' ')    # next 从start到end取元素
                    for idx, ele in enumerate(prev_phrase):
                        if idx < 3:
                            new_patterns.append(ele)
                        else:
                            break
                    for idx, ele in enumerate(next_phrase):
                        if idx < 3:
                            new_patterns.append(ele)
                        else:
                            break
    print('<<< find new patterns done')
    return new_patterns


def append_new_pattern():
    patterns = find_new_pattern()
    patt2counts = {}

    if len(patterns) > 0:
        with open('new_pattern_words.txt', 'w') as f:
            for pattern in patterns:
                f.write(pattern + '\n')
                if pattern.lower() in patt2counts.keys():
                    patt2counts[pattern.strip().lower()] += 1
                else:
                    patt2counts[pattern.strip().lower()] = 1
    else:
        print('\n', '==>', 'new pattern not found', '<==', '\n')

    # append 模式打开 pattern_words.txt
    with open('pattern_words.txt', 'a') as f:
        f.write('\n')
        for key in patt2counts.keys():
            if key.isalpha() and patt2counts[key] >= 100:
                f.write(key.lower() + ' ' + str(patt2counts[key]) + '\n')


if __name__ == '__main__':
    append_new_pattern()
