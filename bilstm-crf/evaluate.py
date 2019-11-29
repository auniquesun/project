#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2019 *** (for blind review)
Date: 2019/11/14
"""

from model.data_utils import CoNLLDataset
from model.ner_model import NERModel
from model.config import Config

from os import listdir
from os.path import join, isfile


def align_data(data):
    """Given dict with lists, creates aligned strings

    Adapted from Assignment 3 of CS224N

    Args:
        data: (dict) data["x"] = ["I", "love", "you"]
              (dict) data["y"] = ["O", "O", "O"]

    Returns:
        data_aligned: (dict) data_align["x"] = "I love you"
                           data_align["y"] = "O O    O  "

    """
    spacings = [max([len(seq[i]) for seq in data.values()])
                for i in range(len(data[list(data.keys())[0]]))]
    data_aligned = dict()

    # for each entry, create aligned string
    for key, seq in data.items():
        str_aligned = ""
        for token, spacing in zip(seq, spacings):
            str_aligned += token + " " * (spacing - len(token) + 1)

        data_aligned[key] = str_aligned

    return data_aligned



def interactive_shell(model):
    """Creates interactive shell to play with model

    Args:
        model: instance of NERModel

    """
    way = input("choose the way of evaluation, please input number \n"
    "                ----interactive(0)/batch(1): ")
    if way == '0':
        model.logger.info("""
    This is an interactive mode.
    To exit, enter 'exit'.
    You can enter a sentence like
    input> Deep Residual Learning for Image Recognition """)

        while True:
            try:
                # for python 2
                sentence = raw_input("input> ")
            except NameError:
                # for python 3
                sentence = input("input> ")

            words_raw = sentence.strip().split(" ")

            if words_raw == ["exit"]:
                break

            preds = model.predict(words_raw)
            to_print = align_data({"input": words_raw, "output": preds})

            for key, seq in to_print.items():
                model.logger.info(seq)
    elif way == '1':
        model.logger.info("""
                >>> Results of prediction of the BiLSTM + CRF model
                >>> will be saved in other/BiLSTM+CRF.results\n""")
        # origin solution
        # gt_name = input('please enter groudtruth number: ')
        # with open('../other/groundtruth/' + gt_name + '.txt') as fin, \
                # open('../other/BiLSTM+CRF.results', 'a') as fout:
        gt_path = '../other/groundtruth/'
        for f in listdir(gt_path):
            if isfile(join(gt_path, f)) is True:
                print('*************', f, '*************')
                with open(join(gt_path, f)) as fin, \
                    open(join('../other/', 'BiLSTM+CRF.results'), 'a') as fout:
                    lines = fin.readlines()
                    if len(lines) % 3 != 0:
                        raise Exception('>>> File', f, 'format ERROR\n')

                    words, labels, preds = None, None, None
                    true, false = 0, 0
                    tp, fp, fn, tn = 0, 0, 0, 0
                    for idx, line in enumerate(lines):  # idx 从0开始                        
                        if idx % 3 == 1:
                            fout.write(line)
                            words = line.strip().split(' ')
                        elif idx % 3 == 2:
                            preds = model.predict(words)
                            fout.write(' '.join(preds) + '\n')
                            labels = line.strip().split(' ')
                            if len(labels) != len(preds):
                                print('>>>', str(idx), 'ERROR: #labels != #preds', '<<<')
                                print('>>>', str(idx), len(labels), len(preds), '<<<')
                                print('labels:', labels)
                                print('preds:', preds)
                            
                            for (label, pred) in zip(labels, preds):
                                if label == pred:
                                    true += 1
                                    if label == 'P' or label == 'M':
                                        tp += 1
                                    else:
                                        tn += 1
                                else:
                                    false += 1
                                    if (label == 'P' or label == 'M') and pred == 'O':
                                        fn += 1
                                    elif (pred == 'P' or pred == 'M') and label == 'O':
                                        fp += 1
                        elif idx % 3 == 0:
                            fout.write(line)
                    if true+false:
                        # print('#true:', true, ', #false:', false)
                        print("loss:", false/(true+false))
                        print("acc:", true/(true+false))
                        precision, recall = tp/(tp+fp), tp/(tp+fn)
                        print('precision:', precision)
                        print('recall:', recall)
                        print('f1 score:', 2*precision*recall/(precision+recall))
                    else:
                        print('both true and false are 0')
                print()
    else:
        raise Exception('>>>Value of way matches nothing, please check your input')


def main():
    # create instance of config
    config = Config()

    # build model
    model = NERModel(config)
    model.build()
    model.restore_session(config.dir_model)

    option = input('>>>>> input the number of your option --\n'
                    'evaluate_on_testset(0)/interactive_shell(1): '
                )
    if option == '0':
        # 直接进去predict就行，没必要在test上evaluate，当然是可以的
        # create dataset
        test = CoNLLDataset(config.filename_test, config.processing_word,
                            config.processing_tag, config.max_iter)
        # evaluate and interact
        model.evaluate(test)
    elif option == '1':
        interactive_shell(model)
    else:
        raise Exception('--> The number should be 0 or 1. -->')


if __name__ == "__main__":
    main()
