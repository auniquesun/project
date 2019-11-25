#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# Copyright 2019 *** (for blind review)
# Time:2019/11/14
"""

from preprocess.preprocess import Preprocess

if __name__ == '__main__':
    """
    从语料中构建训练数据的步骤:    
    a. select 选择标题行
    b. 从标题行迭代发现 new pattern words
    b. 根据pattern words构建pattern + phrase行 --> build_standard_pattern
    c. 根据pattern + phrase构建标签数据 --> build_standard_data
    """
    option = input('build which ——\n\t\t select//pattern/balance/data/validate/title/skipgram?: ')
    build = Preprocess()
    # 从数据集挑选title
    if option == 'select':
        build.select_title_from_dataset()
    if option == 'balance':
        build.make_balance()
    # 验证生成的标签数据格式是否正确
    elif option == 'validate':
        build.validate_standard_data()
    elif option == 'title':
        build.build_title_with_patt()
    # 建立含有 pattern word 的标题的pattern文件，例 "1, P: with, multi-armed bandit, constraints"
    elif option == 'pattern':
        build.build_standard_pattern()
    # 构建训练数据
    elif option == 'data':
        build.build_standard_data()
    elif option == 'skipgram':
        build.build_patt_skipgram()
    else:
        raise Exception('input error, please check your input')
