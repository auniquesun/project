  #!/usr/bin/env bash

  python bert_seq_labeling.py\
    --task_name="sequence labeling"  \
    --do_lower_case=False \
    --crf=False \
    --do_train=True   \
    --do_eval=True   \
    --do_predict=True \
    --do_gt=False \
    --data_dir=data_new   \
    --vocab_file=bert/cased_L-12_H-768_A-12/vocab.txt  \
    --bert_config_file=bert/cased_L-12_H-768_A-12/bert_config.json \
    --init_checkpoint=bert/cased_L-12_H-768_A-12/bert_model.ckpt   \
    --max_seq_length=22   \
    --train_batch_size=64   \
    --learning_rate=2e-5   \
    --num_train_epochs=4.0   \
    --output_dir=./output/result_dir

# perl 是一个命令，具体文档可以自行查阅，conlleval.pl是一个脚本，用来评估序列标注模型的预测效果
# 为啥不用这个默认的评估脚本的，因为我的数据集，和 conll 还是不太一样的，直接用会有问题，precision recall f1都没打出来
# perl conlleval.pl -d '\t' < ./output/result_dir/label_test.txt

# 这是关于 label_test.txt 文件格式的一些说明，来自官方文档 https://www.clips.uantwerpen.be/conll2003/ner/
# The example deals with text chunking, a task which uses the same output format as this named entity task.
#  The program requires the output of the NER system for each word to be appended to the corresponding line 
#  in the test file, with a single space between the line and the output tag. Make sure you keep the empty 
#  lines in the test file otherwise the software may mistakingly regard separate entities as one big entity.
