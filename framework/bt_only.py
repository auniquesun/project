#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright 2019 *** (for blind review)
# Time:2019/11/14
"""

from os import listdir
from os.path import join, isfile

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools, nltk, string

    # set the dir of nltk_data, input your own
    nltk_data_dir = input('the directory of nltk_data: ')
    nltk.data.path.append(nltk_data_dir)

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


def predict_with_rule(sentences):
    patterns = []
    with open('../pattern_words.txt') as fin:
        lines = fin.readlines()
        for line in lines:
            if len(line.strip()) > 0:
                patterns.append(line.strip())
    # print('len(patterns):', len(patterns))
    labels = []
    for sentence in sentences:
        words = [word.lower() for word in sentence.split(' ')]
        if any(word in words for word in patterns):
            # find intersection between words and patterns
            inters = set(words).intersection(patterns)
            flag = None
            for inter in inters:
                # flag to record whether inter == 'for' or not
                if inter == 'for':
                    flag = True
                else:
                    flag = False
                # applying chunking operation to two parts split by inter
                idx = words.index(inter)
                former = extract_candidate_chunks(' '.join(words[:idx]))
                latter = extract_candidate_chunks(' '.join(words[idx+1:]))

                label = ''
                for word in words:
                    if words.index(word) < idx and len(former) and word in former[0]:
                        if flag:
                            label += 'M '
                        else:
                            label += 'P '
                    elif words.index(word) > idx and len(latter) and word in latter[0]:
                        if flag:
                            label += 'P '
                        else:
                            label += 'M '
                    else:
                        label += 'O '
                labels.append(label)
                break   # just select one pattern word

        elif 'based' in words and 'on' in words:
            label = ''
            idx1 = words.index('based')
            idx2 = words.index('on')
            if idx2 - idx1 == 1:
                former = extract_candidate_chunks(' '.join(words[:idx1]))
                latter = extract_candidate_chunks(' '.join(words[idx2+1:]))
                for word in words:
                    if words.index(word) < idx1 and len(former) and word in former[0]:
                        label += 'P '
                    elif words.index(word) > idx2 and len(latter) and word in latter[0]:
                        label += 'M '
                    else:
                        label += 'O '
            else:
                label = 'O '
                label *= len(words)
            labels.append(label)

        else:
            label = 'O '
            label *= len(words)
            labels.append(label)

    return labels


def evaluate_on_gt():
    gt_path = 'groundtruth'
    for f in listdir(gt_path):
        print('*************', f, '*************')
        with open(join(gt_path, f)) as fin, \
                open('rule-based.groundtruth', 'a') as fout:
            lines = fin.readlines() # the data type of 'lines' is a list, which function predict_with_rule needs.

            if len(lines)%3 != 0:
                raise Exception('>>> File', f, 'format ERROR\n')

            true, false = 0, 0
            tp, fp, fn, tn = 0, 0, 0, 0
            titles = []
            for idx, line in enumerate(lines):
                if idx % 3 == 1:
                    titles.append(line)
            preds = predict_with_rule(titles)

            # print('len(titles):', len(titles))
            # print('len(lines):', len(lines))
            # print('len(preds):', len(preds))
            for idx, pred in enumerate(preds):
                fout.write(lines[idx*3])    # blank line or commented line
                fout.write(lines[idx*3 + 1])    # title
                fout.write(pred + '\n')   # pred

                pred, label = pred.strip().split(' '), lines[idx*3 + 2].strip().split(' ')
                if len(pred) != len(label):
                    print('>>>', idx, 'ERROR: #labels != #preds',         '<<<')
                    print('>>>', idx, len(label), len(pred), '<<<')
                    print('label:', label)
                    print('pred:', pred)

                for (p, l) in zip(pred, label):
                    if p == l:
                        true += 1
                        if l == 'P' or l == 'M':
                            tp += 1
                        else:
                            tn += 1
                    else:
                        false += 1
                        if (l == 'P' or l == 'M') and p == 'O':
                            fn += 1
                        elif (p == 'P' or p == 'M') and l == 'O':
                            fp += 1
            if true+false:
                print('#true:', true, ', #false:', false)
                print("acc:", true/(true+false))
                print('#tp:', tp, '#fp:', fp, '#fn:', fn, '#tn', tn)
                precision, recall = tp/(tp+fp), tp/(tp+fn)
                print('precision:', precision)
                print('recall:', recall)
                print('f1 score:', 2*precision*recall/(precision+recall))
            else:
                print('both true and false are 0')
        print()


def evaluate_on_dataset():
    option = input('evaluate on dev_set(0)/test_set(1), please inpute the number: ')
    if option == '0':
        input_file = '../sequence-labeling/data/dev-mag/dev.txt'
        output_file = 'rule-based.mag.devset'
    elif option == '1':
        input_file = '../sequence-labeling/data/test-mag/test.txt'
        output_file = 'rule-based.mag.testset'
    else:
        raise ValueError('the value of "option" should be 0 or 1.')
    titles, labels = [], []

    with open(input_file) as fin, open(output_file, 'w') as fout:
        title, label = [], []
        lines = fin.readlines()
        for line in lines:
            if len(line.strip()) > 0:
                tokens = line.strip().split(' ')
                title.append(tokens[0])
                label.append(tokens[1])
            else:
                if len(title) > 0 and len(label) > 0:
                    titles.append(' '.join(title))
                    labels.append(' '.join(label))
                    title.clear()
                    label.clear()
        # the following function needs a 'list' as the parameter,
        # each element in the list stands for a title
        preds = predict_with_rule(titles)

        print('len(titles):', len(titles))
        print('len(labels):', len(labels))
        print('len(preds):', len(preds))

        # for testing purpose
        # for (ti,pr) in zip(titles, preds):
        #     print(ti, '\n', pr)
        # print(titles[22919])
        # print(preds[25229])

        correct, wrong = 0, 0
        tp, fp, fn, tn = 0, 0, 0, 0
        for idx, (label, pred) in enumerate(zip(labels, preds)):
            fout.write(titles[idx] + '\n')
            fout.write(pred + '\n')
            label = [l for l in label.split(' ') if len(l) > 0]
            pred = [p for p in pred.split(' ') if len(p) > 0]
            print(idx, 'len(label) =', len(label), label)
            print(idx, 'len(pred) =', len(pred), pred)
            assert (len(label) == len(pred)), "both the label and pred should have same size."
            for (l, p) in zip(label, pred):
                if l == p:
                    correct += 1
                else:
                    wrong += 1
                if l == p and (l == 'M' or l == 'P'):
                    tp += 1
                elif l == p and l == 'O':
                    tn += 1
                elif l != p and l == 'O' and (p == 'M' or p == 'P'):
                    fp += 1
                elif l != p and p == 'O' and (l == 'M' or l == 'P'):
                    fn += 1
            fout.write('\n')
        if correct+wrong:
            print('#correct:', correct, ', #wrong:', wrong)
            print("acc:", correct/(correct+wrong))
            print('#tp:', tp, '#fp:', fp, '#fn:', fn, '#tn', tn)
            precision, recall = tp/(tp+fp), tp/(tp+fn)
            print("precision:", precision)
            print("recall:", recall)
            print("f1:", 2*precision*recall/(precision+recall))
        else:
            print('both #correct and #wrong are 0')


if __name__ == '__main__':
    # evaluate_on_gt()
    evaluate_on_dataset()
