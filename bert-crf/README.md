# BERT for Sequence Labeling
Fine-tuning Google's BERT for sequence tagging on datasets provided by our framework. The original version contains some hard codes and lacks corresponding annotations, which is inconvenient to understand. So in this updated version, there are some new ideas and tricks on data preprocessing and layer design that can help you quickly implement the fine-tuning model. You just need to try to modify crf_layer or softmax_layer.

### Folder Description:
```
BERT-CRF
|____ bert                          # need git from [here](https://github.com/google-research/bert)
|____ cased_L-12_H-768_A-12	    # need download from [here](https://storage.googleapis.com/bert_models/2018_10_18/cased_L-12_H-768_A-12.zip)
|____ data		            # train data
|____ middle_data	            # middle data (label id map)
|____ output			    # output (make this directory before training, to store final model and predict results)
|____ bert_seq_labeling.py	    # main code
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
----------------------  Dataset AMiner  ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7906833325079923                  P = 0.7919823755221399
R = 0.7926380817222233                  R = 0.7924725641308076
F = 0.7910506245517833                  F = 0.7916600288130168
Acc = 0.9670364200289844                Acc = 0.9675561200586048

----------------------   Dataset MAG    ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.8012156426333235                  P = 0.8012306470266802
R = 0.797628219229244                   R = 0.7978190562644601
F = 0.799364999295328                   F = 0.7994794137057118
Acc = 0.9756189136514605                Acc = 0.97562357004914

----------------------    Dataset PWC   ----------------------
Acc = 0.8816631130063965
P = 0.7295724687025752
R = 0.7318144284167052
F = 0.7222391857712832
```

* crf=True
* max_seq_length=22
* do_lower_case=False
* num_train_epochs=4.0
```
----------------------  Dataset AMiner  ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7848891464980013                  P = 0.785924500269172
R = 0.7979176083810365                  R = 0.798387824573747
F = 0.7910808622390874                  F = 0.7918655979658572
Acc = 0.9662644075142551                Acc = 0.9670334431947744

----------------------  Dataset MAG     ----------------------
** >>> Dev Dataset **                   ** >>> Test Dataset **
P = 0.7952392958391172                  P = 0.7952655201733481
R = 0.7994229564705185                  R = 0.7993341159311225
F = 0.7972944458518203                  F = 0.7972569439194267
Acc = 0.9737125633190528                Acc = 0.9736713175640963

----------------------    Dataset PWC   ----------------------
Acc = 0.8802352521832115
P = 0.7288195177952838
R = 0.730829494349792
F = 0.7211068086339468
```

### reference:

[1] https://arxiv.org/abs/1810.04805

[2] https://github.com/google-research/bert
