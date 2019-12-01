#! usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Copyright 2019 *** (for blind review)
Date: 2019/11/14
"""

import argparse
from util import Preprocess

if __name__ == '__main__':
    """
    从语料中构建训练数据的步骤:    
    a. select 选择标题行
    b. 从标题行迭代发现 new pattern words
    b. 根据pattern words构建pattern + phrase行 --> build_standard_pattern
    c. 根据pattern + phrase构建标签数据 --> build_standard_data
    """
    parser = argparse.ArgumentParser(description='Some preprocess tasks you need to finish.')
    parser.add_argument('--select', help='select titles from the dataset randomly', action='store_true')
    parser.add_argument('--balance', help='make balance between positive and negative examples', action='store_true')
    parser.add_argument('--validate', help='validate the data format', action='store_true')
    parser.add_argument('--skipgram', help='get skipgrams around pattern word', action='store_true')
    args = parser.parse_args()

    prep = Preprocess()
    
    if args.select:
        prep.select_title_from_dataset()
    elif args.balance:
        prep.make_balance()
    elif args.validate:
        prep.validate_standard_data()
    elif args.skipgram:
        prep.build_patt_skipgram()
    else:
        raise Exception('Invalid argument, please check your input')
