#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
# Copyright 2019 *** (for blind review)
# Time:2019/11/14
"""

class Preprocess:
    def __init__(self):
        self.line_index = 0

    def make_balance(self):
        patt_file = input('fin >>> please input the pattern file: ')
        title_file = input('fout <<< please input the title file: ')
        with open('../data/title/' + 'title1.txt') as fin, open('../data/pattern/' + patt_file) as fin_patt, \
                open('../data/title/' + title_file, 'w') as fout:
            lines = fin.readlines()
            patts = fin_patt.readlines()
            for patt in patts:
                blocks = patt.split(', ')
                if len(blocks) > 0:
                    num = int(blocks[0])
                    fout.write(lines[num-1])


    def build_standard_data(self):
        print('>> starting building standard data')
        file_patt = input('fin > enter pattern file name: ')
        file_title = input('fin > enter title file name: ')
        file_train = input('fout < enter train file name: ')
        with open('../data/pattern/' + file_patt) as fin_pattern, open('../data/title/' + file_title) as fin_title, open('../data/' + file_train, 'w') as fout:
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


    def extract_candidate_chunks(self, text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
        import itertools, nltk, string

        nltk.data.path.append('/home/guanhua/sunhongyu/iGitRepo/project/other/nltk_data')
        # exclude candidates that are stop words or entirely punctuation
        punct = set(string.punctuation)
        stop_words = set(nltk.corpus.stopwords.words('english'))

        # tokenize, POS-tag, and chunk using regular expressions
        chunker = nltk.chunk.regexp.RegexpParser(grammar)
        sents = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]
        tagged_sents = nltk.pos_tag_sents(sents, lang='eng')
        all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                        for tagged_sent in tagged_sents))

        # join constituent chunk words into a single chunked phrase
        candidates = [' '.join(word for word, pos, chunk in group).lower() for key, group in itertools.groupby(all_chunks, lambda word__pos__chunk: word__pos__chunk[2] != 'O') if key]

        return [cand for cand in candidates if cand not in stop_words and not all(char in punct for char in cand)]


    def build_standard_pattern(self):
        print('>> starting building standard pattern')
        patterns = []
        with open('pattern_words.txt') as fin:
            lines = fin.readlines()
            for line in lines:
                if len(line.strip()) > 0 and '#' not in line:
                    patterns.append(line.strip())

        pos_examples, neg_examples = [], []
        file_title = input('fin > enter title file name: ')
        file_patt = input('fout < enter pattern file name: ')
        file_title_real = input('fout < enter real title file name: ')
        with open('../data/title/' + file_title) as fin, open('../data/pattern/' + file_patt, 'w') as fout, \
                open('../data/title/' + file_title_real, 'w') as fout_real:
            lines = fin.readlines()
            for index, line in enumerate(lines):
                if len(pos_examples) >= 500000 and len(neg_examples) >= 500000:
                    break
                if len(line.strip()) != 0:
                    tokens = line.split(' ')
                    tokens = [token for token in tokens if len(token) > 0]
                    
                    if len(tokens):
                        print(index+1, '-->', tokens[0], '-->')
                    if len(tokens) > 0 and tokens[0][-1] == ':':
                        del tokens[0]
                    
                    tokens_lower = [token.lower() for token in tokens]
                    
                    count = 0
                    written_pattern = False
                    written_none = False
                    for pattern in patterns:
                        flag = False
                        
                        if pattern == 'based on':
                            if 'based' in tokens_lower and 'on' in tokens_lower:
                                if tokens_lower.index('on') - tokens_lower.index('based') == 1:
                                    flag = True
                        if pattern in tokens_lower or flag:
                            
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
                                    written_pattern = True
                            else:
                                """
                                句子中存在pattern word，但是len(former)，len(latter)中至少一个为0
                                例，Using GLRPPR (and other P2Rx Centers) to Identify 
                                Hazardous Substance Reduction Resources
                                从这个例子想到另一个pattern，using ... to ...
                                """                       
                                written_none = True
                        if pattern not in tokens_lower and flag == False:
                            count += 1
                        if written_pattern:
                            break
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


    def line_N_K(self, lines):
        import json
        import enchant
        from random import randint
        d = enchant.Dict('en_US')

        titles = []
        N = input('within function "line_N_K", please input N: ')
        for i in range(int(N) * 1000):
            r = randint(0, len(lines)-1)
            print('randint:', r)
            title = json.loads(lines[r])['title']
            if d.check(title[0]) and d.check(title[len(title)-1]):
                titles.append(title)
        return titles


    def select_title_from_dataset(self):
        from os.path import join
        print('>> starting building standard title')
        prefix = '/home/guanhua/sunhongyu/data/text'
        dataset = input('input dataset name: aminer/mag: ')
        
        files = []
        if dataset == 'aminer':
            files.extend(['dblp-ref-0.json', 'dblp-ref-1.json', 'dblp-ref-2.json', 'dblp-ref-3.json'])
        elif dataset == 'mag':
            files.extend(['mag_papers_0.txt', 'mag_papers_1.txt', 'mag_papers_2.txt', 'mag_papers_3.txt'])

        file_title = input('fout < enter title file name: ')
        with open ('../data/title/' + file_title, 'w') as fout:
            for f in files[3:4]:
                with open(join(prefix, dataset, f)) as fin:
                    lines = fin.readlines()
                    #print(type(lines))
                    titles = self.line_N_K(lines)
                    for title in titles:
                        fout.write(title + '\n')
        print('<< build title done')


    def validate_standard_data(self):
        valid_name = input('enter the file name to be validated: ')
        with open('../data/' + valid_name) as fin:
            lines = fin.readlines()
            for index, line in enumerate(lines):
                if len(line.strip()) > 0:
                    if len(line.strip().split(' ')) == 1:
                        # lines that are invalid
                        print('index: ', index+1, 'line: ', line)
        print('[ ' + valid_name + 'is valid' + ' ]')


    def build_patt_skipgram(self):
        print('>> starting getting pattern skipgram')
        file_title = input('fin > enter title file name: ')
        file_patt_sg = input('fout < enter pattern skipgram file name: ')
        with open('../data/title/' + file_title) as fin_title, \
                open('pattern_words.txt') as fin_patt_words, \
                open('../data/skipgram/' + file_patt_sg, 'w') as fout_patt_sg:
            lines_title = fin_title.readlines()
            print('lines: ' + str(len(lines_title)))
            patt_words = fin_patt_words.readlines()
            patt_words = [patt_word.strip().lower() for patt_word in patt_words if len(patt_word.strip()) > 0]
            print(patt_words)
            for index, line_title in enumerate(lines_title):
                words = [word.lower() for word in line_title.strip().split(' ')]
                for patt_word in patt_words:
                    if patt_word in words:
                        before_patt, after_patt = '',''
                        idx = words.index(patt_word)
                        if idx < 3:
                            before_patt = ' '.join(words[:idx])
                        else:
                            before_patt = ' '.join(words[idx-3:idx])
                        if len(words) - idx < 3:
                            # here is a premise: patt_word was not the last word in the title
                            after_patt = ' '.join(words[idx+1:])
                        else:
                            after_patt = ' '.join(words[idx+1:idx+4])
                        fout_patt_sg.write(str(index+1) + ', P: ' + patt_word + ', ' + before_patt + ' __ ' + after_patt + '\n')
        print('<< build pattern skipgram done')


    def build_title_with_patt(self):
        print('>> starting selecting title with pattern')
        file_patt = input('fin > enter pattern file name: ')
        file_title = input('fin > enter title file name: ')
        file_select = input('fout < enter select file name: ')
        with open('../data/pattern/' + file_patt) as fin_pattern, open('../data//title/' + file_title) as fin_title, open('../data//title/' + file_select, 'w') as fout:
            lines_pattern = fin_pattern.readlines()
            lines_title = fin_title.readlines()
            for line_pattern in lines_pattern:
                line_index = int(line_pattern.split(', ')[0])
                fout.write(lines_title[line_index-1])
        print('<< select title done')
