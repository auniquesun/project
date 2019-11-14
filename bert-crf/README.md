# BERT Sequence Labeling
Fine-tuning Google's BERT for sequence tagging on datasets provided by our framework. The original version contains some hard codes and lacks corresponding annotations, which is inconvenient to understand. So in this updated version,there are some new ideas and tricks on data preprocessing and layer design that can help you quickly implement the fine-tuning model. You just need to try to modify crf_layer or softmax_layer.

### Folder Description:
```
BERT-CRF
|____ bert                          # need git from [here](https://github.com/google-research/bert)
|____ cased_L-12_H-768_A-12	    # need download from [here](https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip)
|____ data		            # train data
|____ middle_data	            # middle data (label id map)
|____ output			    # output (final model, predict results)
|____ bert_seq_labeling.py		    # mian code
|____ run.sh    		    # run model and eval result

```


### Usage:
```
bash run.sh
```

### What's in run.sh:
```
python bert_seq_labeling.py\
    --task_name="Sequence Labeling"  \
    --do_lower_case=False \
    --crf=False \
    --do_train=True   \
    --do_eval=True   \
    --do_predict=True \
    --data_dir=data   \
    --vocab_file=cased_L-12_H-768_A-12/vocab.txt  \
    --bert_config_file=cased_L-12_H-768_A-12/bert_config.json \
    --init_checkpoint=cased_L-12_H-768_A-12/bert_model.ckpt   \
    --max_seq_length=128   \
    --train_batch_size=32   \
    --learning_rate=2e-5   \
    --num_train_epochs=3.0   \
    --output_dir=./output/result_dir
```

**Notice:** cased model was recommened, according to [this](https://arxiv.org/abs/1810.04805) paper. CoNLL-2003 dataset and perl Script comes from [here](https://www.clips.uantwerpen.be/conll2003/ner/)


### Results
#### Parameter setting:
* crf=False
* max_seq_length=22
* do_lower_case=False
* num_train_epochs=4.0
```
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7906833325079923                  P = 0.7919823755221399
R = 0.7926380817222233                  R = 0.7924725641308076
F = 0.7910506245517833                  F = 0.7916600288130168
Acc = 0.9670364200289844                Acc = 0.9675561200586048
```

* crf=True
* max_seq_length=22
* do_lower_case=False
* num_train_epochs=4.0
```
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7848891464980013                  P = 0.785924500269172
R = 0.7979176083810365                  R = 0.798387824573747
F = 0.7910808622390874                  F = 0.7918655979658572
Acc = 0.9662644075142551                Acc = 0.9670334431947744
```


### reference:

[1] https://arxiv.org/abs/1810.04805

[2] https://github.com/google-research/bert